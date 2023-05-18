import gradio as gr
from dictionary_lookup.helper.index import Engine
from json import dumps

engine = Engine()


def show_search_result(query):
    resp = engine.search(query=query)
    result = resp[0][0].dict

    result["id"] = int(result["id"])

    return dumps(result, indent=4)


search_engine = gr.Interface(
    show_search_result,
    [
        gr.Textbox(
            label="Search",
            info="Enter your query",
            lines=1,
            value="A bed of roses",
        )
    ],
    gr.Code(
        value="",
        language="json",
        label="Result",
    ),
)
if __name__ == "__main__":
    search_engine.launch()
