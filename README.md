# R.B Electricals & Enterprises — Website

Static website for R.B Electricals & Enterprises, Govt. Certified Class-1 Licensed Electrical Contractor, Ropena Agrahara, Bengaluru.

- Pages: Home, About, Services, Projects & Clients, Contact (with Google Map and WhatsApp quote form)
- SEO: page titles/descriptions, Open Graph, LocalBusiness + FAQ structured data, `sitemap.xml`, `robots.txt`
- Hosting: Vercel (auto-deploys on every push to `main`)

## Editing content
Business details, services and clients live in `tools/build.py`. After editing, run:

```
python3 tools/build.py
```

Set `SITE_URL` to the live domain when it changes, e.g. `SITE_URL=https://www.example.in python3 tools/build.py`.

## Project photos
Add real photos as `assets/img/projects/<client-name>.jpg` (e.g. `acko-technology-pvt-ltd.jpg`) and rebuild; they replace the placeholder covers automatically.
