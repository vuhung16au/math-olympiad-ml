import { MetadataRoute } from 'next'
import { getAvailableBooklets } from '@/lib/booklets'
import { SITE_URL } from '@/lib/og-metadata'

export default function sitemap(): MetadataRoute.Sitemap {
  const booklets = getAvailableBooklets()
  
  const bookletEntries = booklets.map((booklet) => ({
    url: `${SITE_URL}/booklets/${booklet.slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  return [
    {
      url: SITE_URL,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${SITE_URL}/faq`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...bookletEntries,
  ]
}
