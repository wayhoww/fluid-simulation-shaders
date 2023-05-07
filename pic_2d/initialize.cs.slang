import common;

RWStructuredBuffer<ParticleData> Particle;


[numthreads(1, 1, 1)]
void main(uint3 thread_id: SV_DispatchThreadID) {
    if (thread_id.x == 0 && thread_id.y == 0 && thread_id.z == 0) {
        var vars = get_static_variables();
        vars.grid_size = uint2(1, 1); // set in later pass
        vars.frame_count += 1;
        set_static_variables(vars);
    }
}