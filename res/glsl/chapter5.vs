#version 410 core

layout(location = 0) in vec3 Position;
layout(location = 1) in vec3 Color;

out vec3 fragmentColor;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
  gl_Position = projection * view * model * vec4(Position,1);
  fragmentColor = Color;
}
