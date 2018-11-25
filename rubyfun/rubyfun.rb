#! /usr/bin/env ruby

puts "- - - - - - - - - - - - - - - -"

num = 1

while num <= 10
    puts num
    num += 1
end

puts "- - - - - - - - - - - - - - - -"

puts "Hello. I am a ruby program. Please enter a number to square: "
number = gets.chomp.to_f

def square(number)
    squared = number * number
    return squared.to_s
end

puts "Your number is: " + number.to_s
puts "Your number squared is: " + square(number)

puts "- - - - - - - - - - - - - - - -"

if __FILE__ == $0
    puts "This program is being run directly, not 'required'."
end

=begin
year = 1972
puts case year
        when 1970..1979: "Seventies"
        when 1980..1989: "Eighties"
        when 1990..1999: "Nineties"
    end
=end

puts "x"
=begin
  this is a block comment
  You can put anything you like here!

  puts "y"
=end
puts "z"

require 'tk'

root = TkRoot.new { title "Hello, World!" }
TkLabel.new(root) do
   text 'Hello, World!'
   pack { padx 15 ; pady 15; side 'left' }
end
Tk.mainloop

##
#
