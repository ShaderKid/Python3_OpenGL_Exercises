#version 410 core

in vec3 fragmentColor;
out vec3 color;

void main() {
  //float depth = gl_FragCoord.z / gl_FragCoord.w;
  color = fragmentColor;
}
