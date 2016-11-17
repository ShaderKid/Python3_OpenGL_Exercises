#version 410 core

in vec3 Position_w;

out vec3 color;

uniform float time;

void main() {

  float dist = distance(vec3(cos(time)*2,sin(time)*2,sin(time)*10), Position_w);
  float val = abs(sin(dist*3-time*10));
  //float l = length(Position_w.z - sin(time)*10);
  //float val = 1-l*3;
  //color = vec3(0,val,0);
  if (val > 0.98) {
    color = vec3(val,val,0);
  } else {
    color = vec3(0,0,0);
  }
}
