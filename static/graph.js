path = 'data/pitcher_graph_data.json'
console.log(path)

d3.json(path).then((data) => {
    console.log(data)
    
    const svg = d3.select('svg');
    const height = svg.attr('height');
    const width = svg.attr('width');
    const margin = {top: 20, right: 0, bottom: 0, left: 20};
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const chartArea = svg.append('g')
        .attr('transform',`translate(${margin.left},${margin.top})`);

    const plate_x_Extent = d3.extent(data['plate_x']);
    const plate_x_Scale = d3.scaleLinear().domain(plate_x_Extent).range([0, chartWidth]);

    const plate_z_Extent = d3.extent(data['plate_z']);
    const plate_z_Scale = d3.scaleLinear().domain(plate_z_Extent).range([chartHeight,0]);

    
        for (let i = 0; i < data['plate_x'].length; i++) {
            svg.append('circle')
                .attr('r',3)
                .attr('cx', plate_x_Scale(data['plate_x'][i]))
                .attr('cy', plate_z_Scale(data['plate_z'][i]))
                .style('fill', data['indicator'][i]);
            }
    })