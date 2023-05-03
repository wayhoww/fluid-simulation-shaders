import common;

RWTexture2D<float4> Velocity;
RWTexture2D<float4> Data;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;

    if (length(iMouseCoordinate - float2(thread_id.xy)) < 20) {
        if (iMouseLeftButtonDown) {
            Data[thread_id.xy] = float4(1, 0, 0, 1);
        }

        float2 mouse_velocity = (iMouseCoordinate - iMouseLastCoordinate) / DELTA_TIME * CELL_SIZE;
        if (length(mouse_velocity) > 1e-3) {
            Velocity[thread_id.xy] = float4(mouse_velocity, 0, 0);
        }
    }
}
