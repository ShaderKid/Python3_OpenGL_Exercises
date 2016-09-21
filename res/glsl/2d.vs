#version 410 core

layout(location = 0) in vec2 Position;
layout(location = 1) in vec3 Color;

out vec3 fragmentColor;

uniform mat4 projection;

void main() {
  gl_Position = projection * vec4(Position, 0, 1);
  fragmentColor = Color;
}
