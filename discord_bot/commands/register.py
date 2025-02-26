from discord import app_commands
import discord
from utils.scrapper_type import ScrapperType
from config.logger_config import setup_logger
from utils.scrapper_category import ScrapperCategory

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
            for choice in ScrapperCategory.get_category_choices()
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
                for choice in ScrapperCategory.get_category_choices()
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
        choices = ScrapperCategory.get_scrapper_choices(self.category)
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
            scrapper_type = ScrapperType.from_str(self.board)
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

            if self.interaction.client.scrapper_config.add_scrapper(
                channel_id,
                channel_name,
                channel_type,
                scrapper_type,
                guild_name,
            ):
                # 등록 성공 시 '완료' 메시지로 변경
                await self.interaction.edit_original_response(content="✅ 완료")
                await followup.send(
                    content=f"이 {channel_type}을(를) {scrapper_type.get_korean_name()} 알림을 받을 채널로 등록했습니다."
                )
                if channel_type == "server-channels":
                    logger.info(
                        f"서버 채널에서 등록: 채널 ID - {channel_id} | 서버 이름 - {guild_name} | 채널 이름 - {channel_name} | 스크래퍼 타입 - {scrapper_type.get_korean_name()}"
                    )
                else:
                    logger.info(
                        f"DM에서 등록: 사용자 ID - {channel_id} | 사용자 이름 - {channel_name} | 스크래퍼 타입 - {scrapper_type.get_korean_name()}"
                    )
            else:
                # 이미 등록된 경우
                await self.interaction.edit_original_response(content="❗ 실패")
                await followup.send(
                    content=f"이미 이 {channel_type}은(는) {scrapper_type.get_korean_name()} 알림을 받도록 등록되어 있습니다."
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


class DeleteView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=180)
        self.interaction = interaction
        self.category = None
        self.board = None
        self._namespace = {"category": None, "board": None}

    # 1. @discord.ui.select 데코레이터가 아래 메서드를 감싸서 Select UI 컴포넌트를 생성
    # 2. 생성된 Select 컴포넌트는 자동으로 self.select_category 속성으로 저장됨
    # 3. placeholder와 options는 Select 컴포넌트의 초기 설정값이 됨
    @discord.ui.select(
        placeholder="게시판 카테고리를 선택하세요",
        options=[
            discord.SelectOption(label=choice["name"], value=choice["value"])
            for choice in ScrapperCategory.get_category_choices()
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
                for choice in ScrapperCategory.get_category_choices()
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

        await interaction.response.edit_message(
            content="삭제 중...",
            view=None,
        )
        await self.unregister_notice(interaction.followup)

    def update_board_select(self):
        if not self.category:
            return

        choices = ScrapperCategory.get_scrapper_choices(self.category)
        self.select_board.options = [
            discord.SelectOption(label=choice["name"], value=choice["value"])
            for choice in choices
        ]

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def cancel_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self._namespace = {"category": None, "board": None}
        await interaction.response.edit_message(
            content="명령어가 취소되었습니다.", view=None
        )

    async def unregister_notice(self, followup):
        try:
            scrapper_type = ScrapperType.from_str(self.board)
            if isinstance(self.interaction.channel, discord.DMChannel):
                channel_id = str(self.interaction.user.id)
                channel_name = self.interaction.user.name
                channel_type = "direct-messages"
                guild_name = None
            else:
                if not self.interaction.permissions.administrator:
                    await followup.send(
                        "이 명령어는 관리자 권한이 필요합니다.", ephemeral=True
                    )
                    return
                channel_id = str(self.interaction.channel_id)
                channel_name = self.interaction.channel.name
                channel_type = "server-channels"
                guild_name = self.interaction.guild.name

            if self.interaction.client.scrapper_config.remove_scrapper(
                channel_id, channel_type, scrapper_type
            ):
                await self.interaction.edit_original_response(content="✅ 완료")
                await followup.send(
                    content=f"이 {channel_type}에서 {scrapper_type.get_korean_name()} 알림이 삭제되었습니다."
                )
                if channel_type == "server-channels":
                    logger.info(
                        f"서버 채널에서 삭제: 채널 ID - {channel_id} | 서버 이름 - {guild_name} | 채널 이름 - {channel_name} | 스크래퍼 타입 - {scrapper_type.get_korean_name()}"
                    )
                else:
                    logger.info(
                        f"DM에서 삭제: 사용자 ID - {channel_id} | 사용자 이름 - {channel_name} | 스크래퍼 타입 - {scrapper_type.get_korean_name()}"
                    )
            else:
                await self.interaction.edit_original_response(content="❗ 실패")
                await followup.send(
                    content=f"이 {channel_type}에는 {scrapper_type.get_korean_name()} 알림이 등록되어 있지 않습니다."
                )
        except Exception as e:
            logger.error(f"알림 삭제 중 오류 발생: {e}")
            await self.interaction.edit_original_response(content="❌ 오류 발생")
            await followup.send(content="알림 삭제 중 오류가 발생했습니다.")

    async def on_timeout(self):
        try:
            self._namespace = {"category": None, "board": None}
            await self.interaction.edit_original_message(
                content="시간이 초과되어 명령어가 취소되었습니다.", view=None
            )
        except:
            pass


async def setup(bot):
    """공지 등록/삭제 관련 명령어들을 봇에 등록합니다."""

    @bot.tree.command(name="게시판_선택", description="알림을 받을 게시판을 선택합니다")
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
            view = DeleteView(interaction)
            await interaction.response.send_message(
                "삭제할 게시판을 선택해주세요:", view=view, ephemeral=True
            )
        except Exception as e:
            logger.error(f"알림 삭제 중 오류 발생: {e}")
            await interaction.response.send_message(
                "알림 삭제 중 오류가 발생했습니다.", ephemeral=True
            )

    @bot.tree.command(
        name="선택된_게시판", description="현재 선택된 게시판 목록을 보여줍니다"
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
            scrapper_type_list = (
                interaction.client.scrapper_config.get_channel_scrappers(channel_id)
            )

            if scrapper_type_list:
                # 등록된 스크래퍼 목록을 한글명으로 변환
                scrapper_names = [
                    f"- {ScrapperType.from_str(scrapper_type).get_korean_name()}"
                    for scrapper_type in scrapper_type_list
                ]
                message = f"**현재 {channel_type}에 등록된 알림:**\n" + "\n".join(
                    scrapper_names
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
