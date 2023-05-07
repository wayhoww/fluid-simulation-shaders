import common;

Texture2D<float4> GridVelocity;
RWTexture2D<float2> Divergence;

[numthreads(16, 16, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z) {
        return;
    }

    float2 vel_0 = GridVelocity[thread_id.xy + int2(1, 0)].xy;
    float2 vel_1 = GridVelocity[thread_id.xy + int2(-1, 0)].xy;
    float2 vel_2 = GridVelocity[thread_id.xy + int2(0, 1)].xy;
    float2 vel_3 = GridVelocity[thread_id.xy + int2( 0,-1)].xy;

    float divergence = 0.5 * (vel_0.x - vel_1.x + vel_2.y - vel_3.y) / GRID_CELL_SIZE;

    Divergence[thread_id.xy] = divergence, 0.0f, 0.0f, 0.0f;
}
