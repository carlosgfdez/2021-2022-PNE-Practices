import turtle  # this is the part where our object´´ behaviour is defined.

smart = turtle.Turtle()
# Loop 4 times. Everything i want to repeat is indented by for spaces.

for i in range(4):
    smart.foward(50)
    smart.right(90)

# this isn´t indented, so we areen´´ repeating it
turtle.done()