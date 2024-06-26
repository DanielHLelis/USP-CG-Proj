// vi: filetype=glsl
#version 410 core

// camera position
uniform vec3 u_viewPos;

// light sources
uniform vec3 u_ambientColor;
uniform float u_ambientIntensity;

#define MAX_LIGHTS 4
uniform int u_lightCount;
uniform vec3 u_lightPos[MAX_LIGHTS];
uniform vec3 u_lightColors[MAX_LIGHTS];
uniform vec3 u_lightDecay[MAX_LIGHTS];
uniform float u_lightIntensity_d[MAX_LIGHTS];
uniform float u_lightIntensity_s[MAX_LIGHTS];

// lighting parameters
uniform vec3 u_kd;
uniform vec3 u_ks;
uniform vec3 u_ka;
uniform float u_ns;
uniform float u_d;

// lighting toggle
uniform bool u_ignoreLighting;


// vertex data
in vec2 out_texture;
in vec3 out_normal;
in vec3 out_fragPos;

// material properties
uniform sampler2D samplerTexture;

// output color
out vec4 fragColor;

void main() {
  // Try load texture. If there is not a texture, it will be vec4(0.0, 0.0, 0.0, 1.0)
  vec4 composed_kd = texture(samplerTexture, out_texture) + vec4(u_kd, 0.0);

  if (u_ka.x > 2.0) discard; // deleteme

  // Material properties
  vec3 kd = vec3(composed_kd.x, composed_kd.y, composed_kd.z);
  vec3 ka = kd; // todo: add ka as texture too
  vec3 ks = u_ks; // todo: add ks as texture too
  float d = min(composed_kd.a, u_d);

  // Handle alpha depth issues
  if (d < 0.5) discard;

  if (u_ignoreLighting) {
    fragColor = vec4(kd, d);
    return;
  }

  // Fragment normal
  vec3 normal = normalize(out_normal);
  // View direction, from fragment to camera
  vec3 viewDir = normalize(u_viewPos - out_fragPos);

  // Compute ambient light
  vec3 ambient = ka * u_ambientIntensity * u_ambientColor;

  vec3 result = vec3(0.0);

  for (int i = 0; i < u_lightCount; i++) {
    // Compute light direction, from fragment
    vec3 lightDir = normalize(u_lightPos[i] - out_fragPos);

    // Compute attenuation
    float distance = length(u_lightPos[i] - out_fragPos);
    float attenuation = 1.0 / (u_lightDecay[i].x + u_lightDecay[i].y * distance + u_lightDecay[i].z * distance * distance);
    attenuation = clamp(attenuation, 0.0, 1.0);

    // Diffuse light
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = kd * diff * u_lightColors[i] * u_lightIntensity_d[i];

    // Specular light
    vec3 reflectDir = reflect(-lightDir, normal); // Half vector
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_ns);
    vec3 specular = ks * spec * u_lightColors[i] * u_lightIntensity_s[i];

    result += (diffuse + specular) * attenuation;
  }

  fragColor = vec4(ambient + result * (1.0 - u_ambientIntensity), d);
}
