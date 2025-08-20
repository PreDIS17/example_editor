document.addEventListener("DOMContentLoaded", async () => {
  const HeaderTool = window.Header || window.EditorJSHeader || null;
  const ListTool   = window.List   || window.EditorJSList   || null;
  const CodeTool   = window.Code   || window.EditorJSCode   || null;
  const QuoteTool  = window.Quote  || window.EditorJSQuote  || null;

  const tools = {};
  if (HeaderTool) tools.header = { class: HeaderTool, inlineToolbar: ['link'] };
  if (ListTool)   tools.list   = { class: ListTool, inlineToolbar: true };
  if (CodeTool)   tools.code   = { class: CodeTool };
  if (QuoteTool)  tools.quote  = { class: QuoteTool, inlineToolbar: true };

  if (Object.keys(tools).length === 0) console.warn("No Editor.js tools found.");

  // Данные из Django draft.content_md
  const initial = (window.initialMarkdown || "").trim();
  const data = initial ? { blocks: [{ type: "paragraph", data: { text: initial } }] } : {};

  let editor;
  try {
    editor = new EditorJS({
      holder: "editorjs",
      placeholder: "Write your markdown here...",
      tools,
      data
    });
  } catch (e) {
    console.error("EditorJS init error:", e);
    return;
  }

  // Функция для отправки Markdown на сервер
  async function autosave() {
    try {
      const output = await editor.save();
      // Собираем текст всех блоков как Markdown
      const markdownText = output.blocks.map(b => {
        if (b.data) {
          if (b.data.text) return b.data.text;
          if (b.data.code) return "```\n" + b.data.code + "\n```";
        }
        return "";
      }).join("\n\n");

      await fetch(window.autosaveUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": window.csrfToken,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "content=" + encodeURIComponent(markdownText)
      });
      // console.log("Autosaved");
    } catch (err) {
      console.error("Autosave failed:", err);
    }
  }

  setInterval(autosave, 5000);
});
