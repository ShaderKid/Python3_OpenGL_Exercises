#version 410 core

layout(location = 0) in vec3 Position;

void main() {
    gl_Position = mat4(vec4(1.0/800,0,0,0), vec4(0,1.0/600,0,0), vec4(0,0,1,0), vec4(0,0,0,1)) * vec4(Position,1);
}
