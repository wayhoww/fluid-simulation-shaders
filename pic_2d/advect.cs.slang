import common;

RWStructuredBuffer<ParticleData> Particle;
RWTexture2DArray<int> GridVelocityFixed;

[numthreads(64, 1, 1)]
void main(uint3 thread_id: SV_DispatchThreadID) {
    var vars = get_static_variables();
    let particle_count = vars.get_particle_count();

    if(thread_id.x >= particle_count) {
        return;
    }

    var particle = Particle[thread_id.x];

    if (!particle.inside_boundary()) {
        return;
    }

    particle.location += particle.velocity * DELTA_TIME;
    Particle[thread_id.x] = particle;

    // particle to grid
    float2 grid_location = particle.get_grid_location();
    uint2 base_grid_location = uint2(floor(grid_location));
    [unroll]
    for(uint i = 0; i < 2; i++) {
        for(uint j = 0; j < 2; j++) {
            let grid_index = base_grid_location + uint2(i, j);
            if(grid_index.x < 0 || grid_index.y < 0 || grid_index.x >= vars.grid_size.x || grid_index.y >= vars.grid_size.y) {
                continue;
            }

            let grid_particle_distance = grid_location - float2(grid_index);
            let weight = linear_bspine(grid_particle_distance.x) * linear_bspine(grid_particle_distance.y);

            let delta_value = float4(particle.velocity, 1) * weight;
            
            [unroll]
            for (uint i = 0; i < 3; i++) {
                InterlockedAdd(GridVelocityFixed[uint3(grid_index, i)], encode_fixed_point(delta_value[i]));
            }
        }
    }
}