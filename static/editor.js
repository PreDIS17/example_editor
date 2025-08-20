document.addEventListener("DOMContentLoaded", () => {
  // Инициализация Codex Editor
  const editor = new EditorJS({
    holder: "editor",
    placeholder: "Write your markdown here...",
    data: {
      blocks: [
        {
          type: "paragraph",
          data: { text: window.initialMarkdown || "" }
        }
      ]
    },
    tools: {
      // Подключаем Markdown-плагин
      markdown: {
        class: window.EditorJSMarkdown
      }
    }
  });

  async function autosave() {
    const output = await editor.save();
    const markdownText = output.blocks.map(b => b.data.text).join("\n");

    fetch(window.autosaveUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": window.csrfToken,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: "content=" + encodeURIComponent(markdownText)
    });
  }

  // Автосохранение каждые 5 секунд
  setInterval(autosave, 5000);
});
