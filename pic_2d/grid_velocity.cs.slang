import common;

Texture2DArray<int> GridVelocityFixed;
RWTexture2D<float4> GridVelocity;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID) {
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z) {
        return;
    }

    float3 grid_velocity;
    for(uint i = 0; i < 3; i++) {
        grid_velocity[i] = decode_fixed_point(GridVelocityFixed[uint3(thread_id.xy, i)]);
    }

    if (abs(grid_velocity.z) > 1e-7) {
        GridVelocity[thread_id.xy] = float4(grid_velocity.xy, 0, 0) / grid_velocity.z;
    } else {
        GridVelocity[thread_id.xy] = float4(0, 0, 0, 0);
    }
}