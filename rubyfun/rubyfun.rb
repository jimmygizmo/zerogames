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


##
#
