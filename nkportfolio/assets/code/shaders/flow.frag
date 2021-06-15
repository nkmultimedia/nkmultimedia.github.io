// Author: @patriciogv - 2015
// Title: Metaballs

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(0.050,-0.020)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

void main() {
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;
    vec3 mask = vec3(.0);

    // Scale
    st *= 5.;

    // Tile the space
    vec2 i_st = floor(st);
    vec2 f_st = fract(st);

    float m_dist = 1.;  // minimum distance
    for (int j= -1; j <= 1; j++ ) {
        for (int i= -1; i <= 1; i++ ) {
            // Neighbor place in the grid
            vec2 neighbor = vec2(float(i),float(j));

            // Random position from current + neighbor place in the grid
            vec2 offset = random2(i_st + neighbor);

            // Animate the offset
            offset.x = 0.396 + (u_time/100.0) * -0.300*cos(u_time + 8.955*offset.x);
            //offset.y = u_time/10000.0 * sin(u_time + offset.y);

            // Position of the cell
            vec2 pos = neighbor + offset - f_st;

            // Cell distance
            float dist = length(pos);

            // Metaball it!
            m_dist = min(m_dist, m_dist*dist);
        }
    }

    // Draw cells
    mask += step(0.124, m_dist);
    
    vec3 lavaDepthMask = mask + smoothstep(0.124, 0.100, m_dist);
    
    
    float bgMask = smoothstep(0.000, 2.5, st.y);    
    float bgMask2 = smoothstep(5., 2.5, st.y);
    float bgMaskFinal = bgMask * bgMask2;
	vec3 bgColor1 = vec3(0.462,0.185,0.770) * bgMaskFinal * mask;
    vec3 bgColor2 = vec3(0.153,0.061,0.255) * (1.0-bgMaskFinal*mask);
    
    vec3 bgColor = bgColor1 + bgColor2;
    
    vec3 lava = vec3(0.410,0.095,0.000) * (1.0-mask) * (1.0-lavaDepthMask);
    vec3 lava2 = vec3(1.0, 0.0, 0.0) * (1.0-mask) *  lavaDepthMask;
    //lava *= lavaDepthMask;
    vec3 color = lava + lava2 + bgColor;


    gl_FragColor = vec4(vec3(color),1.0);
}
