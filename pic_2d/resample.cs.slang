import common;

RWStructuredBuffer<ParticleData> Particle;
Texture2DArray<float4> GridVelocity;

[numthreads(64, 1, 1)]
void main(uint3 thread_id: SV_DispatchThreadID) {
    var vars = get_static_variables();
    let particle_count = vars.get_particle_count();

    if(thread_id.x >= particle_count) {
        return;
    }

    var particle = Particle[thread_id.x];
    particle.velocity = float2(0, 0);

    float2 grid_location = particle.get_grid_location();
    uint2 base_grid_location = uint2(floor(grid_location));

    [unroll]
    for(uint i = 0; i < 2; i++) {
        for(uint j = 0; j < 2; j++) {
            let grid_index = base_grid_location + uint2(i, j);
            let grid_particle_distance = grid_location - float2(grid_index);
            let weight = linear_bspine(grid_particle_distance.x) * linear_bspine(grid_particle_distance.y);

            particle.velocity += weight * GridVelocity[uint3(grid_index, 0)].xy;
        }
    }

    Particle[thread_id.x] = particle;
}