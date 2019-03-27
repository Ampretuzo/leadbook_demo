function should_abort(url)
  return string.find(url, "/tracking/events")
          or string.find(url, '/log.aspx?')
          or string.find(url, '/logging/messages')
          or string.find(url, 'www.google.com/pagead/')
          or string.find(url, 'googleads.g.doubleclick.net/')
          or string.find(url, 'www.googleadservices.com/')
          or string.find(url, 'google-analytics.com/')
          or string.find(url, 'stats.g.doubleclick.net/')
          or string.find(url, 'adservice.google.com/')
end

function main(splash, args)
  local aborted_requests = {}
  splash:on_request(function (request)
      if should_abort(request.url) then
          table.insert(aborted_requests, request.url)
          request.abort()
      end
  end)
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
    aborted_requests = aborted_requests
  }
end