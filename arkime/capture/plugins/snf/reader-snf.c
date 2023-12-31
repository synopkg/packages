/* reader-snf.c  -- snf instead of libpcap
 *
 * Copyright 2012-2017 AOL Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this Software except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "moloch.h"
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "snf.h"
#include "pcap.h"


extern MolochConfig_t        config;

#define MAX_RINGS 10
#define MAX_PROCS 10

LOCAL snf_handle_t           handles[MAX_INTERFACES];
LOCAL snf_ring_t             rings[MAX_INTERFACES][MAX_RINGS];
LOCAL int                    portnums[MAX_INTERFACES];
LOCAL int                    snfNumRings;
LOCAL int                    snfNumProcs;
LOCAL int                    snfProcNum;
LOCAL uint64_t               totalPktsRead[MAX_INTERFACES][MAX_RINGS];

/******************************************************************************/
int reader_snf_stats(MolochReaderStats_t *stats)
{
    struct snf_ring_stats ss;

    stats->dropped = 0;
    stats->total = 0;

    int i, r;
    int ringStartOffset = (snfProcNum-1)*snfNumRings;
    for (i = 0; i < MAX_INTERFACES && config.interface[i]; i++) {
        for (r = ringStartOffset; r < (ringStartOffset+snfNumRings); r++) {

            // Use the packets read stats accumulated in moloch
            stats->total += totalPktsRead[i][r];

            int err = snf_ring_getstats(rings[i][r], &ss);

            if (err) 
                continue;
            //
            // Miricom reports drops at the NIC level
            // not by ring, so we need to distribute
            // the drops across all rings so we don't overstate.
            // Unfortunately, in multi-process mode you can't tell
            // which process is responsible for the drops, but the
            // inability to tie overrun drops to a particular ring
            // is not possible in the current SNF implementation
            //
            if(r == ringStartOffset) { // Overflows are not reported per ring...
                stats->dropped += (ss.ring_pkt_overflow/snfNumProcs);
            }
            // The previous implementation read this statistic
            // from Myricom, but this is documented to be an estimate.
            // We instead use actual/observed packet counts
            // stats->total += ss.ring_pkt_recv;
        }
    }
    return 0;
}
/******************************************************************************/
LOCAL void *reader_snf_thread(gpointer posv)
{

    long full = (long)posv;
    long pos = full & 0xff;
    long offset = (full >> 8) & 0xff;
    gpointer ring = rings[pos][offset];
    struct snf_recv_req req;

    MolochPacketBatch_t batch;
    moloch_packet_batch_init(&batch);
    while (!config.quitting) {
        int err = snf_ring_recv(ring, -1, &req);
        if (err) {
            if (err == EBUSY || err == EAGAIN || err == EINTR)
                continue;
            LOG("SNF quiting %d", err);
            moloch_quit();
            break;
        }

        MolochPacket_t *packet = MOLOCH_TYPE_ALLOC0(MolochPacket_t);

        packet->pkt           = (u_char *)req.pkt_addr;
        packet->ts.tv_sec     = req.timestamp / 1000000000;
        packet->ts.tv_usec    = (req.timestamp / 1000) % 1000000;
        packet->pktlen        = req.length;
        packet->readerPos     = pos;

        //
        // Add a packet read to the stats accumulator for this ring.
        totalPktsRead[pos][offset] += 1;

        moloch_packet_batch(&batch, packet);

        if (batch.count > 10000)
            moloch_packet_batch_flush(&batch);
    }
    moloch_packet_batch_flush(&batch);
    return NULL;
}
/******************************************************************************/
void reader_snf_start() {
    moloch_packet_set_dltsnap(DLT_EN10MB, config.snapLen);

    int ringStartOffset = (snfProcNum-1)*snfNumRings;
    int i, r;
    for (i = 0; i < MAX_INTERFACES && config.interface[i]; i++) {
        for (r = ringStartOffset; r < (ringStartOffset+snfNumRings); r++) {

            totalPktsRead[i][r] = 0;

            char name[100];
            snprintf(name, sizeof(name), "moloch-snf%d-%d", i, r);
            g_thread_unref(g_thread_new(name, &reader_snf_thread, (gpointer)(long)(i | r << 8)));
        }
        snf_start(handles[i]);
    }
}
/******************************************************************************/
void reader_snf_init(char *UNUSED(name))
{
    struct snf_ifaddrs *ifaddrs;

    snfNumRings = moloch_config_int(NULL, "snfNumRings", 1, 1, MAX_RINGS);
    snfNumProcs = moloch_config_int(NULL, "snfNumProcs", 1, 1, MAX_PROCS);
    snfProcNum  = moloch_config_int(NULL, "snfProcNum", 0, 0, MAX_PROCS);

    // Quick config sanity check for clustered processes
    if (snfNumProcs > 1 && snfProcNum == 0) {
       CONFIGEXIT("Myricom: snfNumProcs set > 1 but snfProcNum not present in config");
    } else {
       snfProcNum = 1;
    }

    int snfDataRingSize = moloch_config_int(NULL, "snfDataRingSize", 0, 0, 0x7fffffff);
    int snfFlags = moloch_config_int(NULL, "snfFlags", -1, 0, -1);

    int err;
    if ( (err = snf_init(SNF_VERSION_API)) != 0) {
        CONFIGEXIT("Myricom: failed in snf_init(%d) = %d", SNF_VERSION_API, err);
    }

    if ((err = snf_getifaddrs(&ifaddrs)) || ifaddrs == NULL) {
        CONFIGEXIT("Myricom: failed in snf_getifaddrs %d", err);
    }

    int ringStartOffset = (snfProcNum-1)*snfNumRings;
    int i, r;
    for (i = 0; i < MAX_INTERFACES && config.interface[i]; i++) {
        struct snf_ifaddrs *ifa = ifaddrs;
        portnums[i] = -1;

        while (ifa) {
            if (strcmp(config.interface[i], ifa->snf_ifa_name) == 0) {
                portnums[i] = ifa->snf_ifa_portnum;
                break;
            }
            ifa = ifa->snf_ifa_next;
        }

        if (portnums[i] == -1 && sscanf(config.interface[i], "snf%d", &portnums[i]) != 1) {
            CONFIGEXIT("Myricom: Couldn't find interface '%s'", config.interface[i]);
        }

        err  = snf_open(portnums[i], snfNumRings * snfNumProcs, NULL, snfDataRingSize, snfFlags, &handles[i]);
        if (err != 0) {
            CONFIGEXIT("Myricom: Couldn't open interface '%s' %d", config.interface[i], err);
        }

        for (r = ringStartOffset; r < (ringStartOffset+snfNumRings); r++) {
            err = snf_ring_open(handles[i], &rings[i][r]);
            if (err != 0) {
                CONFIGEXIT("Mryicom: Couldn't open ring %d for interface '%s' %d", r, config.interface[i], err);
            }
        }

    }

    snf_freeifaddrs(ifaddrs);

    moloch_reader_start         = reader_snf_start;
    moloch_reader_stats         = reader_snf_stats;
}
/******************************************************************************/
void moloch_plugin_init()
{
    moloch_readers_add("snf", reader_snf_init);
}
