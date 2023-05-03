import common;

Texture2D<float4> Pressure;

RWTexture2D<float4> InOutVelocity;

[numthreads(16, 16, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;

    float pressure_0 = Pressure[thread_id.xy + int2( 1, 0)].x;
    float pressure_1 = Pressure[thread_id.xy + int2(-1, 0)].x;
    float pressure_2 = Pressure[thread_id.xy + int2( 0, 1)].x;
    float pressure_3 = Pressure[thread_id.xy + int2( 0,-1)].x;

    float2 gradient = float2(pressure_0 - pressure_1, pressure_2 - pressure_3) * 0.5;
    float2 velocity = InOutVelocity[thread_id.xy].xy - gradient;

    InOutVelocity[thread_id.xy] = float4(velocity, 0.0, 0.0);
}
