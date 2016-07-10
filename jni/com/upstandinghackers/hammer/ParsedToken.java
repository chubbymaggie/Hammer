package com.upstandinghackers.hammer;

public class ParsedToken
{
    public Hammer.TokenType getTokenType()
    {
        int tt = this.getTokenTypeInternal();
        if(0==tt)
            return null;
        return Hammer.tokenTypeMap.get(new Integer(tt));
    }

    public native int getTokenTypeInternal();
    public native int getIndex();
    public native byte getBitOffset();
    public native byte[] getBytesValue();
    public native long getSIntValue();
    public native long getUIntValue();
    public native double getDoubleValue();
    public native float getFloatValue();
    public native ParsedToken[] getSeqValue();
//    public native Object getUserValue();
    public native void setUserTokenType(int typeValue);

    public native void setTokenType(Hammer.TokenType type);
    public native void setIndex(int index);
    public native void setBitOffset(byte offset);
    public native void setBytesValue(byte[] value);
    public native void setSIntValue(long value);
    public native void setUIntValue(long value);
    public native void setDoubleValue(double value);
    public native void setFloatValue(float value);
    public native void setSeqValue(ParsedToken value[]);
//    public native void setUserValue(Object value);
    
//    public native void free();
    public long getInner() {return this.inner;}

    private long inner;
    ParsedToken(long inner) {this.inner=inner;}
}
