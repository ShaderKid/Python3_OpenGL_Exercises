#version 410 core

in vec3 fragmentColor;
in vec3 Position_w;
out vec4 color;

uniform float ball;

void main() {
  float l = abs((Position_w.z - ball)*3);
  if (l > 0.3) {
    color = vec4(fragmentColor,1);
  } else {
    color = vec4(0,max(fragmentColor.g,l),0,1);
  }
}
