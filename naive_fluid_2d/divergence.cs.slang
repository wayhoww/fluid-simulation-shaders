import common;

Texture2D<float4> Velocity;
RWTexture2D<float4> OutDivergence;

[numthreads(16, 16, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;

    float2 vel_0 = Velocity[thread_id.xy + int2( 1, 0)].xy;
    float2 vel_1 = Velocity[thread_id.xy + int2(-1, 0)].xy;
    float2 vel_2 = Velocity[thread_id.xy + int2( 0, 1)].xy;
    float2 vel_3 = Velocity[thread_id.xy + int2( 0,-1)].xy;

    float divergence = 0.5 * (vel_0.x - vel_1.x + vel_2.y - vel_3.y) / CELL_SIZE;

    OutDivergence[thread_id.xy] = float4(divergence, 0.0f, 0.0f, 0.0f);
}
