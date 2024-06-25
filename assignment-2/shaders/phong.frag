// vi: filetype=glsl
#version 410 core

// light sources
#define MAX_LIGHTS 4
uniform int u_lightCount;
uniform vec3 u_ambientColor;
uniform float u_ambientIntensity;
uniform vec3 u_lightPos[MAX_LIGHTS];
uniform vec3 u_lightColors[MAX_LIGHTS];
uniform vec3 u_lightDecay[MAX_LIGHTS];
uniform float u_lightIntensity[MAX_LIGHTS];

// lighting parameters
uniform float u_ka;
uniform float u_kd;
uniform float u_ks;
uniform float u_ns;

// camera position
uniform vec3 u_viewPos;

// vertex data
in vec2 out_texture;
in vec3 out_normal;
in vec3 out_fragPos;

// material properties
uniform sampler2D samplerTexture;

// output color
out vec4 fragColor;

void main() {
  vec3 normal = normalize(out_normal);
  vec3 viewDir = normalize(u_viewPos - out_fragPos);
  vec3 ambient = u_ka * u_ambientIntensity * u_ambientColor;
  vec3 result = vec3(0.0);

  for (int i = 0; i < u_lightCount; i++) {
    vec3 lightDir = normalize(u_lightPos[i] - out_fragPos);
    float distance = length(u_lightPos[i] - out_fragPos);
    float attenuation = 1.0 / (u_lightDecay[i].x + u_lightDecay[i].y * distance + u_lightDecay[i].z * distance * distance);
    vec3 lightColor = u_lightColors[i] * u_lightIntensity[i] * attenuation;
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_ns);
    vec3 specular = u_ks * spec * lightColor;
    vec3 diffuse = u_kd * diff * lightColor;
    result += (diffuse + specular);
  }

  vec4 textureColor = texture(samplerTexture, out_texture);

  fragColor = vec4(ambient + result, 1.0) * textureColor;
}
