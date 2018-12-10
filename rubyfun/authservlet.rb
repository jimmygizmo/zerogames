#! /usr/bin/env ruby

# HTTP authentication for a directory listing

require 'webrick'

include WEBrick

dir = Dir::pwd

port = 4444

authenticate = Proc.new do |req, res|

  HTTPAuth.basic_auth(req, res, '') do |user, password|

    user == 'foo' && password == 'bar'

  end

end

s = HTTPServer.new(:Port => port, :ServerType => Daemon)

s.mount('/', HTTPServlet::FileHandler, dir,

  :FancyIndexing => true,

  :HandlerCallback => authenticate # Hook up the authentication proc.

)

trap('INT') { s.shutdown }

s.start

