# CodeX Editor Integratsiyasi 

## Umumiy ma’lumot

Biz **[CodeX Editor](https://editorjs.io/)** (Editor.js) ni Django loyihamizga integratsiya qildik.  
U oddiy `<textarea>` maydonlarini **blok asosidagi muharrir** bilan almashtiradi va quyidagilarni ta’minlaydi:

- Boy matn formatlash (sarlavhalar, ro‘yxatlar, iqtiboslar, kod bloklari)  
- Markdown uslubida kontent boshqaruvi  
- Kontentni JSON formatida saqlash va osongina HTMLga render qilish  
- Yangi plaginlar va vositalarni qo‘shish imkoniyati  

---

## Nima uchun CodeX Editor?

- **Blok asosidagi zamonaviy tahrir**: kontent bloklarga bo‘lingan, oddiy HTML yoki Markdown emas.  
- **Moslashuvchan saqlash**: kontent JSON formatida saqlanadi va HTMLga render qilinadi.  
- **Kengaytiriladigan**: Header, List, Code, Quote, Image kabi plaginlar bilan ishlaydi.  
- **Autosave qo‘llab-quvvatlanadi**: foydalanuvchi ishini yo‘qotmaydi,avtomatik saqlaydi.  
- **Kelajak uchun tayyor**: boshqa vositalar, eksport formatlari yoki frontend ramkalar bilan oson integratsiya qilinadi.

---

## Django loyihasida ishlatish

### Modellar

- `Draft` — foydalanuvchi uchun vaqtinchalik kontent saqlaydi  
- `Post` — nashr qilingan kontent  
- Har ikkala model ham **Markdown kontent**ni saqlaydi

- `autosave_draft` — kontentni asenxron tarzda saqlaydi  
- `publish_post` — JSON/Markdownni HTMLga o‘giradi va `Post` ob’ektini yaratadi  


### Frontend

- `editor.html` — CodeX Editor instansiyasi va autosave sozlamalari mavjud  
- `editor.js` — Editor.jsni sozlaydi, vositalarni (Header, List, Code, Quote) ro‘yxatga oladi va autosave qiladi  
- Autosave intervalli: har 5 soniyada  

---

## Asosiy vositalar (Tools)

- **Header** — sarlavhalar bloklari  
- **List** — tartiblangan va tartiblanmagan ro‘yxatlar  
- **Code** — fenced kod bloklari  
- **Quote** — inline formatlash bilan iqtiboslar  

Kerak bo‘lsa, boshqa vositalarni (Image, Table, Embed) `editor.js`ga import qilib osongina qo‘shish mumkin.

---
