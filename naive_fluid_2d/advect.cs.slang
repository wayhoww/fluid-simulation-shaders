import common;

Texture2D<float4> Velocity;
Texture2D<float4> Data;

RWTexture2D<float4> OutVelocity;
RWTexture2D<float4> OutData;


[numthreads(16, 16, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;

    float2 velocity = Velocity[thread_id.xy].xy;
    float2 delta_pos = velocity * DELTA_TIME / CELL_SIZE;
    float2 last_pos = thread_id.xy - delta_pos;

    OutVelocity[thread_id.xy] = Velocity.Load(last_pos) * 0.999;
    OutData[thread_id.xy] = Data.Load(last_pos) * 0.995;
}
