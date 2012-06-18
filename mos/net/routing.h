/**
 * Copyright (c) 2008-2012 the MansOS team. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice,
 *    this list of  conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef MANSOS_ROUTING_H
#define MANSOS_ROUTING_H

#include "addr.h"

//===========================================================
// Data types and constants
//===========================================================

typedef enum {
    RD_DROP,      // ignore
    RD_LOCAL,     // receive locally
    RD_UNICAST,   // send/forward as unicast packet
    RD_BROADCAST, // send/forward as broadcast packet
} RoutingDecision_e;

typedef uint16_t Seqnum_t;

enum {
    ROUTING_INFORMATION,
    ROUTING_REQUEST,
};

// routing information, sent out from base station, forwarded by nodes
struct RoutingInfoPacket_s {
    uint8_t packetType;        // ROUTING_INFORMATION
    uint8_t __reserved;
    MosShortAddr rootAddress;  // address of the base station / gateway
    uint16_t hopCount;         // distance from root
    Seqnum_t seqnum;           // sequence number
    uint32_t rootClock;        // used for time sync to calculate the delta
} PACKED;

typedef struct RoutingInfoPacket_s RoutingInfoPacket_t;

typedef struct RoutingRequestPacket_s {
    uint8_t packetType;        // ROUTING_REQUEST
    uint8_t __reserved;
} RoutingRequestPacket_t;

#define ROUTING_PROTOCOL_PORT  112

#if 0
#define ROUTING_ORIGINATE_TIMEOUT   (60 * 1000ul)
#define ROUTING_INFO_VALID_TIME    (180 * 1000ul)
#else // for testing
#define ROUTING_ORIGINATE_TIMEOUT    (5 * 1000ul)
#define ROUTING_INFO_VALID_TIME     (30 * 1000ul)
#endif

#define MAX_HOP_COUNT 16

extern MosShortAddr rootAddress;

extern int32_t rootClockDelta;

//===========================================================
// Procedures
//===========================================================

void initRouting(void);

RoutingDecision_e routePacket(MacInfo_t *info);

#endif