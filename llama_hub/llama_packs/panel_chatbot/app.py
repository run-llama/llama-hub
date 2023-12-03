import os
import pickle
from pathlib import Path

import nest_asyncio
import panel as pn
import param
from llama_index import GPTVectorStoreIndex, download_loader

from llama_hub.github_repo import GithubClient, GithubRepositoryReader

nest_asyncio.apply()

CACHE_PATH = Path(".cache")
CACHE_PATH.mkdir(parents=True, exist_ok=True)

CHAT_GPT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png"
CHAT_GPT_URL = "https://chat.openai.com/"
LLAMA_INDEX_LOGO = (
    "https://cdn-images-1.medium.com/max/280/1*_mrG8FG_LiD23x0-mEtUkw@2x.jpeg"
)
PANEL_LOGO = {
    "default": "https://panel.holoviz.org/_static/logo_horizontal_light_theme.png",
    "dark": "https://panel.holoviz.org/_static/logo_horizontal_dark_theme.png",
}

GITHUB_LOGO = "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
GITHUB_URL = "https://github.com/"
LLAMA_INDEX_URL = "https://www.llamaindex.ai/"
PANEL_URL = "https://panel.holoviz.org/index.html"
GITHUB_COPILOT_LOGO = (
    "https://plugins.jetbrains.com/files/17718/447537/icon/pluginIcon.svg"
)

INDEX_NOT_LOADED = "No repository loaded"
INDEX_LOADED = "Repository loaded"
LOADING_EXISTING_DOCS = "Loading existing docs"
LOADING_NEW_DOCS = "Downloading documents"
LOADING_EXISTING_INDEX = "Loading existing index"
LOADING_NEW_INDEX = "Creating index"
CUTE_LLAMA = Path(__file__).parent / "llama_by_sophia_yang.png"

pn.chat.ChatMessage.default_avatars.update(
    {
        "assistant": GITHUB_COPILOT_LOGO,
        "user": "🦙",
    }
)
pn.chat.ChatMessage.show_reaction_icons = False

LLAMA_FROM = "#6366f1"
LLAMA_TO = "#ec4899"
ACCENT = "#ec4899"  # purple

CSS_FIXES_TO_BE_UPSTREAMED = """
#sidebar {
    padding-left: 5px !important;
    background-color: var(--panel-surface-color);
}
.pn-wrapper {
    height: calc( 100vh - 150px);
}
"""


def _split_and_clean(cstext):
    return cstext.split(",")


class IndexLoader(pn.viewable.Viewer):
    value: GPTVectorStoreIndex = param.ClassSelector(class_=GPTVectorStoreIndex)

    status = param.String(constant=True, doc="A status message")
    reload = param.Boolean(
        default=False,
        label="Full Reload",
        doc="If not checked we will reuse an existing index if possible",
    )

    owner: str = param.String(
        default="holoviz", doc="The repository owner. For example 'holoviz'"
    )
    repo: str = param.String(
        default="panel", doc="The repository name. For example 'panel'"
    )
    filter_directories: str = param.String(
        default="examples,docs,panel",
        label="Folders",
        doc="A comma separated list of folders to include. For example 'examples,docs,panel'",
    )
    filter_file_extensions: str = param.String(
        default=".py,.md,.ipynb",
        label="File Extensions",
        doc="A comma separated list of file extensions to include. For example '.py,.md,.ipynb'",
    )

    _load = param.Event(label="LOAD")

    def __init__(self, load=True):
        super().__init__()

        if load:
            self.load()
        else:
            self._update_status(INDEX_NOT_LOADED)

        self._layout = pn.Column(
            self.param.owner,
            self.param.repo,
            self.param.filter_directories,
            self.param.filter_file_extensions,
            pn.pane.HTML(self.github_url),
            pn.widgets.Button.from_param(
                self.param._load,
                button_type="primary",
                disabled=self._is_loading,
                loading=self._is_loading,
            ),
            self.param.reload,
            pn.pane.Markdown("### Status", margin=(3, 5)),
            pn.pane.Str(self.param.status),
        )

    def __panel__(self):
        return self._layout

    @property
    def _unique_id(self):
        uid = (
            self.owner
            + self.repo
            + self.filter_directories
            + self.filter_file_extensions
        )
        uid = uid.replace(",", "").replace(".", "")
        return uid

    @property
    def _docs_path(self):
        return CACHE_PATH / f"docs_{self._unique_id}.pickle"

    @property
    def _index_path(self):
        return CACHE_PATH / f"index_{self._unique_id}.pickle"

    def _download_docs(self):
        print("Downloading docs ...")

        download_loader("GithubRepositoryReader")

        github_client = GithubClient(os.getenv("GITHUB_TOKEN"))

        filter_directories = _split_and_clean(self.filter_directories)
        filter_file_extensions = _split_and_clean(self.filter_file_extensions)

        loader = GithubRepositoryReader(
            github_client,
            owner=self.owner,
            repo=self.repo,
            filter_directories=(
                filter_directories,
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            filter_file_extensions=(
                filter_file_extensions,
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            verbose=True,
            concurrent_requests=10,
        )
        return loader.load_data(branch="main")

    def _get_docs(self):
        docs_path = self._docs_path
        index_path = self._index_path

        if docs_path.exists():
            self._update_status(LOADING_EXISTING_DOCS)
            with docs_path.open("rb") as f:
                return pickle.load(f)

        self._update_status(LOADING_NEW_DOCS)
        docs = self._download_docs()

        with docs_path.open("wb") as f:
            pickle.dump(docs, f, pickle.HIGHEST_PROTOCOL)

        if index_path.exists():
            index_path.unlink()

        return docs

    def _create_index(self, docs):
        print("Creating index ...")
        return GPTVectorStoreIndex.from_documents(docs)

    def _get_index(self, index):
        index_path = self._index_path

        if index_path.exists():
            self._update_status(LOADING_EXISTING_INDEX)
            with index_path.open("rb") as f:
                return pickle.load(f)

        self._update_status(LOADING_NEW_INDEX)
        index = self._create_index(index)

        with index_path.open("wb") as f:
            pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)
        return index

    @param.depends("status")
    def _is_loading(self):
        return self.status not in [INDEX_LOADED, INDEX_NOT_LOADED]

    @param.depends("status")
    def _is_not_loading(self):
        return self.status in [INDEX_LOADED, INDEX_NOT_LOADED]

    @param.depends("_load", watch=True)
    def load(self):
        self._update_status("Loading ...")
        self.value = None

        if self.reload:
            if self._docs_path.exists():
                self._docs_path.unlink()
            if self._index_path.exists():
                self._index_path.unlink()

        docs = self._get_docs()
        self.value = self._get_index(docs)
        self._update_status(INDEX_LOADED)

    def _update_status(self, text):
        with param.edit_constant(self):
            self.status = text
        print(text)

    @param.depends("owner", "repo")
    def github_url(self):
        text = f"{self.owner}/{self.repo}"
        href = f"https://github.com/{text}"
        return f"<a href='{href}' target='_blank'>{text}</a>"

    @property
    def index_exists(self):
        return self._docs_path.exists() and self._index_path.exists()


def powered_by():
    params = {"height": 40, "sizing_mode": "fixed", "margin": (0, 10)}
    return pn.Column(
        pn.pane.Markdown("### AI Powered By", margin=(10, 5, 10, 0)),
        pn.Row(
            pn.pane.Image(LLAMA_INDEX_LOGO, link_url=LLAMA_INDEX_URL, **params),
            pn.pane.Image(CHAT_GPT_LOGO, link_url=CHAT_GPT_URL, **params),
            pn.pane.Image(PANEL_LOGO[pn.config.theme], link_url=PANEL_URL, **params),
            align="center",
        ),
    )


async def main_component(index: GPTVectorStoreIndex, index_loader: IndexLoader):
    if not index:
        return pn.Column(
            pn.chat.ChatMessage(
                "You are a now a *GitHub Repository assistant*.",
                user="System",
            ),
            pn.chat.ChatMessage(
                "Please **load a GitHub Repository** to start chatting with me. This can take from seconds to minutes!",
                user="Assistant",
            ),
        )

    chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

    async def generate_response(contents, user, instance):
        response = chat_engine.stream_chat(contents)
        text = ""
        for token in response.response_gen:
            text += token
            yield text

    chat_interface = pn.chat.ChatInterface(
        callback=generate_response,
        sizing_mode="stretch_both",
    )
    chat_interface.send(
        pn.chat.ChatMessage(
            "You are a now a *GitHub Repository Assistant*.", user="System"
        ),
        respond=False,
    )
    chat_interface.send(
        pn.chat.ChatMessage(
            f"Hello! you can ask me anything about {index_loader.github_url()}.",
            user="Assistant",
        ),
        respond=False,
    )
    return chat_interface


def create_app():
    pn.extension(sizing_mode="stretch_width", raw_css=[CSS_FIXES_TO_BE_UPSTREAMED])

    index_loader = IndexLoader(load=False)
    pn.state.location.sync(
        index_loader,
        parameters={
            "owner": "owner",
            "repo": "repo",
            "filter_directories": "folders",
            "filter_file_extensions": "file_extensions",
        },
    )

    if index_loader.index_exists:
        index_loader.load()

    i_chat_interface = pn.bind(
        main_component, index=index_loader.param.value, index_loader=index_loader
    )

    return pn.template.FastListTemplate(
        title="Chat with GitHub",
        sidebar=[
            pn.pane.Image(
                CUTE_LLAMA, height=250, align="center", margin=(10, 5, 25, 5)
            ),
            "## Github Repository",
            index_loader,
            powered_by(),
        ],
        main=[i_chat_interface],
        accent=ACCENT,
        main_max_width="1000px",
        main_layout=None,
    )


if pn.state.served:
    create_app().servable()
