import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

const LineChart = () => {
  const svgRef = useRef();
  const containerRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 500, height: 300 });

  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth *.95,
          height: containerRef.current.clientHeight *0.90,
        });
      }
    };

    // Initial dimension setup
    handleResize();

    // Add event listener for resize
    window.addEventListener('resize', handleResize);

    // Cleanup event listener
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    // Dummy data with timestamps
    const data = [
      { timestamp: new Date('2023-01-01T00:00:00Z'), y: 30 },
      { timestamp: new Date('2023-01-02T00:00:00Z'), y: 80 },
      { timestamp: new Date('2023-01-03T00:00:00Z'), y: 45 },
      { timestamp: new Date('2023-01-04T00:00:00Z'), y: 60 },
      { timestamp: new Date('2023-01-05T00:00:00Z'), y: 20 },
      { timestamp: new Date('2023-01-06T00:00:00Z'), y: 90 },
      { timestamp: new Date('2023-01-07T00:00:00Z'), y: 55 },
    ];

    // Clear existing SVG content
    d3.select(svgRef.current).selectAll('*').remove();

    // Create scales
    const xScale = d3.scaleTime()
      .domain(d3.extent(data, d => d.timestamp))
      .range([0, dimensions.width]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.y)])
      .nice()
      .range([dimensions.height, 0]);

    // Create line generator
    const line = d3.line()
      .x(d => xScale(d.timestamp))
      .y(d => yScale(d.y));

    // Append the line path
    d3.select(svgRef.current)
      .append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', 'orange')
      .attr('stroke-width', 2)
      .attr('d', line);

    // Add circles for each data point
    d3.select(svgRef.current)
      .selectAll('.dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', d => xScale(d.timestamp))
      .attr('cy', d => yScale(d.y))
      .attr('r', 5)
      .attr('fill', 'orange')
      .on('click', (event, d) => {
        alert(`Timestamp: ${d.timestamp.toISOString()}\nValue: ${d.y}`);
      });

    // Add x-axis
    d3.select(svgRef.current)
      .append('g')
      .attr('transform', `translate(0, ${dimensions.height})`)
      .call(d3.axisBottom(xScale).ticks(7).tickFormat(d3.timeFormat("%Y-%m-%d")));

    // Add y-axis
    d3.select(svgRef.current)
      .append('g')
      .call(d3.axisLeft(yScale));

  }, [dimensions]); // Update on dimensions change

  return (
    <div ref={containerRef} style={{ width: '100%', height: '300px' }}>
      <svg ref={svgRef} width="100%" height="100%"></svg>
    </div>
  );
};

export default LineChart;
