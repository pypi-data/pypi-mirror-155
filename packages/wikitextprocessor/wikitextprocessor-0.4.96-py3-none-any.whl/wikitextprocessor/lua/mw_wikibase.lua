-- Simplified sub implementation of mw.wikibase for running WikiMedia Scribunto
-- code under Python
--
-- Copyright (c) 2021 Tatu Ylonen.  See file LICENSE and https://ylonen.org

local mw_wikibase = {
}

function mw_wikibase.getEntity(id)
   return nil
end

function mw_wikibase.getEntityIdForTitle(pageTitle, globalSiteId)
   return nil
end

function mw_wikibase.getEntityUrl(id)
   return nil
end

function mw_wikibase.getLabel(id)
   return nil
end

function mw_wikibase.getLabelWithLang(id)
   return nil
end

function mw_wikibase.getLabelByLang(id, languageCode)
   return nil
end

function mw_wikibase.getSitelink(id, globalSiteId)
   return nil
end

function mw_wikibase.getDescription(id)
   return nil
end

function mw_wikibase.getDescriptionWithLang(id)
   return nil
end

function mw_wikibase.isValidEntityId(id)
   return True
end

function mw_wikibase.entityExists(id)
   return False
end

function mw_wikibase.renderSnak(snak)
   return nil
end

function mw_wikibase.formatValue(snak)
   return nil
end

function mw_wikibase.renderSnaks(snaks)
   return nil
end

function mw_wikibase.formatValues(snaks)
   return nil
end

function mw_wikibase.resolvePropertyId(labelOrId)
   return nil
end

function mw_wikibase.getPropertyOrder()
   return {}
end

function mw_wikibase.orderProperties(tbl)
   return tbl
end

function mw_wikibase.getBestStatements(entityId, propertyId)
   return {}
end

function mw_wikibase.getAllStatements(entityId, propertyId)
   return {}
end

function mw_wikibase.getReferencedEntityId(fromEntityId, propertyId, toIds)
   return nil
end

function mw_wikibase.getGlobalSiteId()
   return "enwiktionary"
end

-- Some legacy aliases
mw_wikibase.getEntityObject = mw_wikibase.getEntity
mw_wikibase.label = mw_wikibase.getLabel
mw_wikibase.description = mw_wikibase.getDescription
mw_wikibase.sitelink = mw_wikibase.getSitelink

-- XXX entity object methods; currently we don't return any entities

return mw_wikibase
