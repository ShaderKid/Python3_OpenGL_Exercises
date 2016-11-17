#version 410 core

layout(location = 0) in vec3 Position_m;
layout(location = 1) in vec3 Color;

out vec3 fragmentColor;
out vec3 Position_w;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
  gl_Position = projection * view * model * vec4(Position_m,1);
  Position_w = (model * vec4(Position_m,1)).xyz;
  fragmentColor = Color;
}
