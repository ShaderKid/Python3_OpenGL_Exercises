#version 410 core

layout(location = 0) in vec3 Position_m;

out vec3 Position_w;

uniform mat4 P;
uniform mat4 V;
uniform mat4 M;

void main() {
  gl_Position = P * V * M * vec4(Position_m,1);
  Position_w = (M * vec4(Position_m,1)).xyz;
}
