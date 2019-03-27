function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  splash:runjs([[
    var showEmailButton = document.getElementById('textemail')
    if (showEmailButton) {
      showEmailButton.click()
    }
  ]])
	splash:wait(0.5)
  return {
    -- png = splash:png{render_all=true},
    -- har = splash:har(),
    html = splash:html(),
  }
end