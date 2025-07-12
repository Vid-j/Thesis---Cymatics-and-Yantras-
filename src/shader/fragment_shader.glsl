#version 330

in vec2 uv;
out vec4 fragColor;

uniform float pitch;
uniform float amplitude;

const float PI = 3.1415926538;

// --- Ripple function ---
float ripple(float dist, float shift) {
    return cos(24.0 * dist + shift) / (0.5 + dist);
}

// --- Polar Chladni-like pattern ---
float polarChladni(vec2 p, float n, float m) {
    vec2 center = vec2(0.5, 0.5);
    p = p - center;

    float r = length(p) * 2.0;
    float theta = atan(p.y, p.x);

    return sin(n * theta) * sin(m * r);
}

void main() {
    vec2 center = vec2(0.5, 0.5);
    vec2 pos = uv - center;

    // === Base: Concentric ripples ===
    float base = ripple(length(pos), 0.0);

    // === Extra poles: Rotational symmetry ===
    float rippleSum = 0.0;
    int POLES = int(clamp(floor(pitch), 3.0, 20.0));
    float angleStep = 2.0 * PI / float(POLES);
    float shift = amplitude * 2.0;

    for (int i = 0; i < POLES; ++i) {
        float angle = float(i) * angleStep;
        vec2 dir = vec2(cos(angle), sin(angle));
        vec2 polePos = center + dir * 0.3;
        rippleSum += ripple(length(pos - (polePos - center)), shift);
    }

    // === Polar Chladni ===
    float chladni = polarChladni(uv, pitch * 2.0, amplitude * 2.0);

    // === Weighted blending ===
    float t = smoothstep(1.0, 3.0, pitch);
    float z = mix(base, base + rippleSum + chladni, t);

    // === Add distance-based falloff ===
    z *= exp(-length(pos) * 2.0);

    // === Normalize & threshold to lines ===
    float val = smoothstep(0.015, 0.017, abs(z));
    val *= exp(-length(pos) * 1.5);
    fragColor = vec4(vec3(1.0 - val), 1.0);
}
