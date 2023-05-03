cbuffer PerFrameCB
{
    uint3 iThreads;
    float iTime;
    float iDeltaTime;
    float2 iMousePosition;
    int2 iMouseCoordinate;
    int2 iMouseLastCoordinate;
    bool iMouseLeftButtonDown;
};

extension Texture2D<float4> {
    float4 Load(float2 pos) {
        int2 pos00 = int2(pos);
        int2 pos01 = pos00 + int2(0, 1);
        int2 pos10 = pos00 + int2(1, 0);
        int2 pos11 = pos00 + int2(1, 1);

        float4 data00 = this.Load(int3(pos00, 0));
        float4 data01 = this.Load(int3(pos01, 0));
        float4 data10 = this.Load(int3(pos10, 0));
        float4 data11 = this.Load(int3(pos11, 0));

        float4 data0 = lerp(data01, data00, pos11.y - pos.y);
        float4 data1 = lerp(data11, data10, pos11.y - pos.y);

        float4 data = lerp(data1, data0, pos11.x - pos.x);

        return data;
    }
}

constexpr static float CELL_SIZE = 0.1f;
constexpr static float DELTA_TIME = 0.01f;