import discord
from utils.scraper_type import ScraperType
from config.logger_config import setup_logger
from utils.scraper_category import ScraperCategory
from config.env_loader import ENV

logger = setup_logger(__name__)


class RegisterView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=180)
        self.interaction = interaction
        self.category = None
        self.board = None
        self._namespace = {"category": None, "board": None}

    @discord.ui.select(
        placeholder="게시판 카테고리를 선택하세요",
        options=[
            discord.SelectOption(label=choice["name"], value=choice["value"])
            for choice in ScraperCategory.get_category_choices()
        ],
    )
    async def select_category(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self.category = select.values[0]
        self._namespace["category"] = self.category
        self.update_board_select()
        selected_category = next(
            (
                choice["name"]
                for choice in ScraperCategory.get_category_choices()
                if choice["value"] == select.values[0]
            ),
            "알 수 없는 카테고리",
        )
        self.select_category.placeholder = selected_category

        await interaction.response.edit_message(view=self)

    @discord.ui.select(
        placeholder="게시판을 선택하세요",
        options=[
            discord.SelectOption(label="먼저 카테고리를 선택하세요", value="none")
        ],
    )
    async def select_board(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self.board = select.values[0]
        self._namespace["board"] = self.board

        # UI 제거하고 '등록 중' 메시지 표시
        await interaction.response.edit_message(
            content="등록 중...",
            view=None,
        )
        # 등록 처리 진행
        await self.register_notice(interaction.followup)

    def update_board_select(self):
        if not self.category:
            return

        # 선택된 카테고리의 게시판 목록 가져오기
        choices = ScraperCategory.get_scraper_choices(self.category)
        self.select_board.options = [
            discord.SelectOption(label=choice["name"], value=choice["value"])
            for choice in choices
        ]

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def cancel_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # 내부 namespace 초기화
        self._namespace = {"category": None, "board": None}
        await interaction.response.edit_message(
            content="명령어가 취소되었습니다.", view=None
        )

    async def register_notice(self, followup):
        try:
            scraper_type = ScraperType.from_str(self.board)
            if isinstance(self.interaction.channel, discord.DMChannel):
                channel_id = str(self.interaction.user.id)
                channel_name = self.interaction.user.name
                channel_type = "direct-messages"
                guild_name = None  # DM은 서버가 없음
            else:
                # 서버 채널인 경우 관리자 권한 확인
                if not self.interaction.permissions.administrator:
                    await self.interaction.response.send_message(
                        "이 명령어는 관리자 권한이 필요합니다.", ephemeral=True
                    )
                    return
                channel_id = str(self.interaction.channel_id)
                channel_name = self.interaction.channel.name
                channel_type = "server-channels"
                guild_name = self.interaction.guild.name  # 서버 이름 가져오기

            if self.interaction.client.scraper_config.add_scraper(
                channel_id,
                channel_name,
                channel_type,
                scraper_type,
                guild_name,
            ):
                # 등록 성공 시 '완료' 메시지로 변경
                await self.interaction.edit_original_response(content="✅ 완료")
                await followup.send(
                    content=f"이 {channel_type}을(를) {scraper_type.get_korean_name()} 알림을 받을 채널로 등록했습니다."
                )
                if channel_type == "server-channels":
                    logger.info(
                        f"서버 채널에서 등록: 채널 ID - {channel_id} | 서버 이름 - {guild_name} | 채널 이름 - {channel_name} | 스크래퍼 타입 - {scraper_type.get_korean_name()}"
                    )
                else:
                    logger.info(
                        f"DM에서 등록: 사용자 ID - {channel_id} | 사용자 이름 - {channel_name} | 스크래퍼 타입 - {scraper_type.get_korean_name()}"
                    )
            else:
                # 이미 등록된 경우
                await self.interaction.edit_original_response(content="❗ 실패")
                await followup.send(
                    content=f"이미 이 {channel_type}은(는) {scraper_type.get_korean_name()} 알림을 받도록 등록되어 있습니다."
                )
        except Exception as e:
            logger.error(f"알림 등록 중 오류 발생: {e}")
            await self.interaction.edit_original_response(content="❌ 오류 발생")
            await followup.send(content="알림 등록 중 오류가 발생했습니다.")

    async def on_timeout(self):
        try:
            # 내부 namespace 초기화
            self._namespace = {"category": None, "board": None}
            await self.interaction.edit_original_message(
                content="시간이 초과되어 명령어가 취소되었습니다.", view=None
            )
        except:
            pass


async def setup(bot):
    """공지 등록/삭제 관련 명령어들을 봇에 등록합니다."""

    @bot.tree.command(name="게시판_선택", description=ENV["SELECT_CATEGORY_ANNOUNCEMENT"])
    async def register_notice(interaction: discord.Interaction):
        """공지사항 알림을 등록합니다."""
        try:
            view = RegisterView(interaction)
            await interaction.response.send_message(
                "게시판을 선택해주세요:", view=view, ephemeral=True
            )
        except Exception as e:
            logger.error(f"알림 등록 중 오류 발생: {e}")
            await interaction.response.send_message(
                "알림 등록 중 오류가 발생했습니다.", ephemeral=True
            )

    @bot.tree.command(
        name="게시판_선택취소", description="선택한 게시판의 알림을 취소합니다"
    )
    async def unregister_notice(interaction: discord.Interaction):
        """현재 채널에서 선택한 유형의 공지사항 알림을 삭제합니다."""
        try:
            # 서버 채널인 경우 관리자 권한 확인
            if not isinstance(interaction.channel, discord.DMChannel):
                if not interaction.permissions.administrator:
                    await interaction.response.send_message(
                        "이 명령어는 관리자 권한이 필요합니다.", ephemeral=True
                    )
                    return

            # 채널 정보 설정
            channel_id = (
                str(interaction.user.id)
                if isinstance(interaction.channel, discord.DMChannel)
                else str(interaction.channel_id)
            )
            channel_type = (
                "direct-messages"
                if isinstance(interaction.channel, discord.DMChannel)
                else "server-channels"
            )

            # 등록된 스크래퍼 목록 가져오기
            registered_scrapers = (
                interaction.client.scraper_config.get_channel_scrapers(channel_id)
            )

            if not registered_scrapers:
                await interaction.response.send_message(
                    "현재 등록된 알림이 없습니다.", ephemeral=True
                )
                return

            # 등록된 스크래퍼들의 카테고리 찾기
            registered_categories = set()
            all_categories = ScraperCategory.get_category_choices()

            for category in all_categories:
                category_scrapers = ScraperCategory.get_scraper_choices(
                    category["value"]
                )
                for scraper in category_scrapers:
                    if scraper["value"].lower() in registered_scrapers:
                        registered_categories.add(category["value"])
                        break

            # 등록된 카테고리가 없는 경우 처리
            if not registered_categories:
                await interaction.response.send_message(
                    "현재 등록된 알림이 없습니다.", ephemeral=True
                )
                return

            # 카테고리 선택 메뉴 생성
            category_select = discord.ui.Select(
                placeholder="게시판 카테고리를 선택하세요",
                options=[
                    discord.SelectOption(
                        label=category["name"], value=category["value"]
                    )
                    for category in all_categories
                    if category["value"] in registered_categories
                ],
            )

            # 게시판 선택 메뉴 생성
            board_select = discord.ui.Select(
                placeholder="게시판을 선택하세요",
                options=[
                    discord.SelectOption(label="카테고리를 선택해주세요", value="none")
                ],
            )

            # 카테고리 선택 콜백
            async def category_callback(interaction: discord.Interaction):
                try:
                    selected_category = category_select.values[0]

                    # 선택된 카테고리 이름 찾기
                    selected_category_name = next(
                        (
                            category["name"]
                            for category in all_categories
                            if category["value"] == selected_category
                        ),
                        "알 수 없는 카테고리",
                    )

                    # 카테고리 선택 메뉴의 placeholder 업데이트
                    category_select.placeholder = selected_category_name

                    # 선택된 카테고리의 게시판 중 등록된 것만 필터링
                    category_scrapers = ScraperCategory.get_scraper_choices(
                        selected_category
                    )
                    registered_boards = [
                        scraper
                        for scraper in category_scrapers
                        if scraper["value"].lower() in registered_scrapers
                    ]

                    # 게시판 선택 옵션 업데이트
                    board_select.options = [
                        discord.SelectOption(label=board["name"], value=board["value"])
                        for board in registered_boards
                    ]
                    board_select.placeholder = "게시판을 선택하세요"

                    await interaction.response.edit_message(view=view)

                except Exception as e:
                    logger.error(f"카테고리 선택 중 오류 발생: {e}")
                    await interaction.response.send_message(
                        "카테고리 선택 중 오류가 발생했습니다.", ephemeral=True
                    )

            # 게시판 선택 콜백
            async def board_callback(interaction: discord.Interaction):
                try:
                    selected_board = board_select.values[0]
                    scraper_type = ScraperType.from_str(selected_board)

                    if interaction.client.scraper_config.remove_scraper(
                        channel_id, channel_type, scraper_type
                    ):
                        message = f"✅ 이 {channel_type}에서 {scraper_type.get_korean_name()} 알림이 삭제되었습니다."
                        if channel_type == "server-channels":
                            logger.info(
                                f"서버 채널에서 삭제: 채널 ID - {channel_id} | 서버 이름 - {interaction.guild.name} | 채널 이름 - {interaction.channel.name} | 스크래퍼 타입 - {scraper_type.get_korean_name()}"
                            )
                        else:
                            logger.info(
                                f"DM에서 삭제: 사용자 ID - {channel_id} | 사용자 이름 - {interaction.user.name} | 스크래퍼 타입 - {scraper_type.get_korean_name()}"
                            )
                    else:
                        message = f"❗ 이 {channel_type}에는 {scraper_type.get_korean_name()} 알림이 등록되어 있지 않습니다."

                    await interaction.response.edit_message(content=message, view=None)

                except Exception as e:
                    logger.error(f"게시판 선택 중 오류 발생: {e}")
                    await interaction.response.send_message(
                        "게시판 선택 중 오류가 발생했습니다.", ephemeral=True
                    )

            # 콜백 설정
            category_select.callback = category_callback
            board_select.callback = board_callback

            # View 생성 및 컴포넌트 추가
            view = discord.ui.View(timeout=180)
            view.add_item(category_select)
            view.add_item(board_select)

            # 메시지 전송
            await interaction.response.send_message(
                "취소할 게시판을 선택해주세요:", view=view, ephemeral=True
            )

        except Exception as e:
            logger.error(f"알림 삭제 중 오류 발생: {e}")
            await interaction.response.send_message(
                "알림 삭제 중 오류가 발생했습니다.", ephemeral=True
            )

    @bot.tree.command(
        name="선택된_게시판", description=ENV["CHECK_CATEGORY_ANNOUNCEMENT"]
    )
    async def list_crawlers(interaction: discord.Interaction):
        """현재 채널에 등록된 공지사항 알림 목록을 보여줍니다."""
        try:
            # DM인지 서버 채널인지 확인
            if isinstance(interaction.channel, discord.DMChannel):
                channel_id = str(interaction.user.id)
                channel_type = "direct-messages"
                channel_name = interaction.user.name
            else:
                channel_id = str(interaction.channel_id)
                channel_type = "server-channels"
                channel_name = interaction.channel.name
                guild_name = interaction.guild.name

            # 등록된 스크래퍼 목록 가져오기
            scraper_type_list = interaction.client.scraper_config.get_channel_scrapers(
                channel_id
            )

            if scraper_type_list:
                # 등록된 스크래퍼 목록을 한글명으로 변환
                scraper_names = [
                    f"- {ScraperType.from_str(scraper_type).get_korean_name()}"
                    for scraper_type in scraper_type_list
                ]
                message = f"**현재 {channel_type}에 등록된 알림:**\n" + "\n".join(
                    scraper_names
                )
            else:
                message = f"현재 {channel_type}에 등록된 알림이 없습니다."

            if channel_type == "direct-messages":
                logger.info(
                    f"DM에서 목록 조회: 사용자 ID - {channel_id} | 사용자 이름 - {channel_name}"
                )
            else:
                logger.info(
                    f"서버 채널에서 목록 조회: 채널 ID - {channel_id} | 서버 이름 - {guild_name} | 채널 이름 - {channel_name}"
                )

            await interaction.response.send_message(message, ephemeral=True)

        except Exception as e:
            logger.error(f"알림 목록 조회 중 오류 발생: {e}")
            await interaction.response.send_message(
                "알림 목록 조회 중 오류가 발생했습니다.", ephemeral=True
            )
