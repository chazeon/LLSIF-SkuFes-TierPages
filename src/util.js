import _ from 'lodash'

function calcSpeed(start, end) {
    if (start['rank'] !== end['rank']) return undefined
    let scoreDiff = end['score'] - start['score']
    let timeDiff = end['time'] - start['time']
    let timeUnit = 60 * 60
    return {
        time: end['time'],
        speed: scoreDiff / timeDiff * timeUnit,
        rank: end['rank']
    }
}

function getSpeedOfRank(sorted, interval) {
    let speed = []
    for (let i = 0; i < sorted.length - interval; ++i) {
        let end = sorted[i]
        let start = sorted[i + interval]
        speed.push(calcSpeed(start, end))
    }
    return speed
}

function getSpeedRecords(data, interval) {
    return {
        time: data.time,
        ranks: data.ranks,
        records: _.values(_.mapValues(
            data.records,
            rankrecords => {
                return {
                    rank: rankrecords.rank,
                    data: getSpeedOfRank(rankrecords.data, interval)
                }
            }))

    }
}

function groupScoreRecordByRank(dataset, unit) {
    let time = _.unionBy(_.values(_.mapValues(dataset, 'time')), time => (time / unit | 0) * unit)
    let grouped = _.groupBy(dataset, 'rank')
    let ranks = _.sortBy(_.keys(grouped), (a, b) => parseInt(a) < parseInt(b))
    return {
        ranks, time,
        records: _.map(grouped, (data, rank) => {
            return { data, rank }
        })
    }
}

function groupScoreRecordByRankForce(dataset, unit) {
    let time = _.unionBy(_.values(_.mapValues(dataset, 'time')), time => (time / unit | 0) * unit)
    let grouped = _.groupBy(dataset, 'rank')
    let ranks = _.sortBy(_.keys(grouped), (a, b) => parseInt(a) < parseInt(b))
    return {
        ranks, time,
        records: _.map(grouped, (data, rank) => {
            data = _.unionBy(data, item => (item.time / unit | 0) * unit)
            return { data, rank }
        })
    }
}

export default {
    getSpeedRecords,
    calcSpeed,
    groupScoreRecordByRank,
    groupScoreRecordByRankForce
}