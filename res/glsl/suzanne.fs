#version 410 core

in vec3 Position_w;
in vec3 Normal_c;
in vec3 EyeDirection_c;
in vec3 LightDirection_c;

out vec3 color;

uniform vec3 LightPosition_w;

void main() {
  vec3 LightColor = vec3(1,1,1);
  float LightPower = 50.0f;

  vec3 DiffuseColor = vec3(0.8,0.8,0.8);
  vec3 AmbientColor = vec3(0.1,0.1,0.1) * DiffuseColor;
  vec3 SpecularColor = vec3(0.3,0.3,0.3);

  float distance = length( LightPosition_w - Position_w );

  vec3 n = normalize( Normal_c );
  vec3 l = normalize( LightDirection_c );
  float cosTheta = clamp( dot( n,l ), 0,1);

  vec3 E = normalize(EyeDirection_c);
  vec3 R = reflect(-l,n);
  float cosAlpha = clamp( dot( E,R ), 0,1 );

  color = AmbientColor + DiffuseColor * LightColor * LightPower * cosTheta / (distance*distance) + SpecularColor * LightColor * LightPower * pow(cosAlpha,5) / (distance*distance);
}
