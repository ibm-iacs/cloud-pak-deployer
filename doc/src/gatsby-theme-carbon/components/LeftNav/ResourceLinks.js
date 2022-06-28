import React from 'react';
import ResourceLinks from 'gatsby-theme-carbon/src/components/LeftNav/ResourceLinks';

const links = [
  {
    title: 'GitHub repo',
    href: 'https://github.com/IBM/cloud-pak-deployer',
  },
  {
    title: 'Development setup',
    href: 'https://ibm.github.io/cloud-pak-deployer/development/deployer-development-setup',
  },
  {
    title: 'Carbon',
    href: 'https://www.carbondesignsystem.com',
  },
  {
    title: 'Gatsby Guide',
    href: 'https://gatsby-theme-carbon.now.sh/getting-started',
  }
];

// shouldOpenNewTabs: true if outbound links should open in a new tab
const CustomResources = () => <ResourceLinks shouldOpenNewTabs links={links} />;

export default CustomResources;
