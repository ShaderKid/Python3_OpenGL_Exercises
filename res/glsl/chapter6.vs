#version 410 core

layout(location = 0) in vec3 Position;
layout(location = 1) in vec2 vertexUV;

out vec2 UV;

uniform float time;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() {
  gl_Position = projection * view * model * vec4(Position.x+cos(time)*5, Position.y+sin(time)*5, Position.z,1);
  UV = vertexUV;
}
