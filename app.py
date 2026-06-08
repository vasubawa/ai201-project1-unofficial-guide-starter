import gradio as gr
from query import ask

def handle_query(question):
    result = ask(question)
    
    if result["sources"]:
        sources_text = "\n".join(f"• {source}" for source in result["sources"])
    else:
        sources_text = "No sources found in your documents."
        
    return result["answer"], sources_text

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ UCF Foundation Exam (FE) Study Companion")
    gr.Markdown("An unofficial, grounded RAG assistant utilizing student guides, rules, and crowd-sourced knowledge.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Ask a question about the exam:", 
            placeholder="e.g., What happens if I pass COP 3502 and skip the next available exam?",
            lines=2
        )
    
    with gr.Row():
        btn = gr.Button("Submit Query", variant="primary")
    
    with gr.Row():
        answer_box = gr.Textbox(label="System Response (Grounded)", lines=8, interactive=False)
        
    with gr.Row():
        sources_box = gr.Textbox(label="Retrieved Data Sources:", lines=3, interactive=False)
        
    btn.click(handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, sources_box])

if __name__ == "__main__":
    print("🚀 Launching Gradio interface...")
    demo.launch()