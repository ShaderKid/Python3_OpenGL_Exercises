#version 410 core

in vec3 fragmentColor;
out vec4 color;

void main() {
  //float depth = gl_FragCoord.z / gl_FragCoord.w;
  color = vec4(fragmentColor,1);
}
