to generate `document_linked`

```sh
pandoc document_linked.md -o document_linked.pdf -f markdown -t pdf --standalone --resource-path ./document_assets --template eisvogel
```