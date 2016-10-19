#version 410 core

layout(location = 0) in vec3 Position;

uniform mat4 scale;
uniform mat4 rotation;
uniform mat4 translation;
uniform float time;

void main() {
  gl_Position = mat4(
    vec4(cos(time),sin(time),0,0),
    vec4(-sin(time),cos(time),0,0),
    vec4(0,0,1,0),
    vec4(0,0,0,1)) * vec4(Position, 1);
  //gl_Position = rotation * vec4(Position,1);
  //gl_Position = vec4(Position, 1) * mat4(
  //  vec4(cos(time),-sin(time),0,0),
  //  vec4(sin(time),cos(time),0,0),
  //  vec4(0,0,1,0),
  //  vec4(0,0,0,1)) * mat4(
  //  vec4(sin(time)+1,0,0,0),
  //  vec4(0,sin(time)+1,0,0),
  //  vec4(0,0,1,0),
  //  vec4(0,0,0,1));
}
