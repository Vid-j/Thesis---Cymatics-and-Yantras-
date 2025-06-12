#version 150

uniform sampler2DRect u_yantra;
uniform float u_fft[64];
uniform vec2 u_resolution;
uniform float u_time;

in vec2 vTexCoord;
out vec4 fragColor;

void main() {
    vec2 uv = vTexCoord / u_resolution;
    float dist = distance(uv, vec2(0.5));

    // Map distance to an FFT bin
    int bin = int(dist * 64.0);
    float amp = u_fft[bin];

    // Simple cymatic-like radial animation
    float wave = sin(40.0 * dist - u_time * 2.0);
    float brightness = smoothstep(0.3, 0.0, abs(wave - amp));

    vec3 cymatic = vec3(brightness);

    // Sample yantra texture
    vec4 yantraTex = texture(u_yantra, vTexCoord * u_resolution);

    // Blend visuals
    vec3 finalColor = yantraTex.rgb + cymatic;

    fragColor = vec4(finalColor, 1.0);
}
