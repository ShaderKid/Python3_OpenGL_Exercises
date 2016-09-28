#version 410 core

layout(location = 0) in vec3 Position;
layout(location = 1) in vec2 vertexUV;

out vec2 UV;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
  gl_Position = projection * view * model * vec4(Position,1);
  UV = vertexUV;
}
