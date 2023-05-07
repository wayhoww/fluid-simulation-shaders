import common;

RWStructuredBuffer<ParticleData> Particle;
RWTexture2D<float4> GridData;

// constant
float2 get_initial_velocity(float2 grid_uv) {
    let diff = grid_uv - float2(0.5, 0.5);
    if (abs(diff.x) > 0.4 || abs(diff.y) > 0.4) return float2(0, 0);

    return float2(2, 0);
}

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID) {
    var vars = get_static_variables();
    vars.grid_size = iThreads.xy;

    if (thread_id.x == 0 && thread_id.y == 0 && thread_id.z == 0) {
        set_static_variables(vars);
    }

    let center_location = vars.grid_size * GRID_CELL_SIZE * float2(0.2, 0.5);
    let thread_location = thread_id.xy * GRID_CELL_SIZE;

    if(length(thread_location - center_location) < 1) {
        GridData[thread_id.xy] = float4(1, 0, 0, 1);
    }

    let particle_base_index = (thread_id.y * (vars.grid_size.x - 1) + thread_id.x) * 9;
    for(int i = 0; i < 9; i++) {
        let particle_index = particle_base_index + i;
        var particle = Particle[particle_index];
        if (particle_index >= vars.get_particle_count()) break;
        if (length(particle.location - center_location) < 1) {
            particle.velocity = float2(5, 0);
            Particle[particle_index] = particle;
        }
    }

    if (vars.is_the_first_frame()) {
        if(int(thread_id.x) < int(vars.grid_size.x) - 1 && int(thread_id.y) < int(vars.grid_size.y) - 1) {
            // initialize particles
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    var particle : ParticleData; 
                    particle.set_location_from_grid(float2(thread_id.xy) + float2(i, j) / 3.0);
                    
                    let grid_uv = (thread_id.xy + float2(i, j)) / (vars.grid_size - float2(1, 1));
                    particle.velocity = float2(0, 0);

                    let particle_index = particle_base_index + i * 3 + j;
                    Particle[particle_index] = particle;
                }
            }
        }
    }
}