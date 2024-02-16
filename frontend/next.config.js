/**@type {import('next').NextConfig} */
module.exports = {
    async rewrites() {
      return [
        {
          source: '/api/:path',
          destination: 'https://apalucha.kaktusgame.eu/api/:path' 
        }
      ]
    }
}

