# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/builder.py
# Compiled at: 2019-10-27 06:58:29
# Size of source mod 2**32: 25669 bytes
"""
Helper functions and information for building DFBA models.
"""
import warnings, logging, libsbml
from sbmlutils import factory
from sbmlutils.factory import *
from sbmlutils.factory import PORT_SUFFIX
from sbmlutils import comp
from sbmlutils import fbc
from sbmlutils.dfba import utils
MODEL_FRAMEWORK_FBA = 'fba'
MODEL_FRAMEWORK_ODE = 'ode'
MODEL_FRAMEWORKS = {MODEL_FRAMEWORK_FBA: ['SBO:0000624'], 
 MODEL_FRAMEWORK_ODE: ['SBO:0000293']}
DT_ID = 'dt'
DT_SIM = 0.1
DT_SBO = 'SBO:0000346'
LOWER_BOUND_DEFAULT = -1000
UPPER_BOUND_DEFAULT = 1000
ZERO_BOUND = 0
LOWER_BOUND_PREFIX = 'lb_'
UPPER_BOUND_PREFIX = 'ub_'
FLUX_BOUND_SBO = 'SBO:0000625'
UPDATE_REACTION_PREFIX = 'update_'
UPDATE_REACTION_SBO = 'SBO:0000631'
UPDATE_PARAMETER_SBO = 'SBO:0000613'
EXCHANGE_REACTION_PREFIX = 'EX_'
EXCHANGE_REACTION_SBO = 'SBO:0000627'
EXCHANGE = 'exchange'
EXCHANGE_IMPORT = 'import'
EXCHANGE_EXPORT = 'export'
FLUX_PARAMETER_PREFIX = 'p' + EXCHANGE_REACTION_PREFIX
DUMMY_REACTION_PREFIX = EXCHANGE_REACTION_PREFIX
DUMMY_SPECIES_ID = 'dummy_S'
DUMMY_SPECIES_SBO = 'SBO:0000291'
DUMMY_REACTION_SBO = 'SBO:0000631'
FLUX_PARAMETER_SBO = 'SBO:0000612'
FLUX_ASSIGNMENTRULE_SBO = 'SBO:0000391'
SBML_LEVEL = 3
SBML_VERSION = 1
SBML_FBC_NAME = libsbml.FbcExtension_getPackageName()
SBML_FBC_VERSION = 2
SBML_COMP_NAME = libsbml.CompExtension_getPackageName()
SBML_COMP_VERSION = 1
libsbml.CompExtension_getPackageName()

def get_framework(model):
    """ Get the framework for the given model object.

    This is the sbo which is set on the respective model/modelDefinition element.

    :param model:
    :return: framework key or None if no framework information could be found.
    """
    if type(model) not in [libsbml.Model, libsbml.ModelDefinition]:
        raise ValueError('Framework must be defined on either Model/ModelDefinition, but given: {}'.format(model))
    else:
        framework = None
        if model.isSetSBOTerm():
            sbo = model.getSBOTermID()
            for fw, sbos in MODEL_FRAMEWORKS.items():
                if sbo in sbos:
                    framework = fw

        else:
            warnings.warn('SBOTerm for modelling framework not set')
    if framework is None:
        warnings.warn('No framework set for: {}'.format(model))
    return framework


def template_doc_fba(model_id):
    """ create template for fba model.

    :param model_id: model identifier
    :return: SBMLDocument
    """
    sbmlns = libsbml.SBMLNamespaces(SBML_LEVEL, SBML_VERSION)
    sbmlns.addPackageNamespace(SBML_FBC_NAME, SBML_FBC_VERSION)
    sbmlns.addPackageNamespace(SBML_COMP_NAME, SBML_COMP_VERSION)
    doc = libsbml.SBMLDocument(sbmlns)
    doc.setPackageRequired(SBML_COMP_NAME, True)
    doc.setPackageRequired(SBML_FBC_NAME, False)
    model = doc.createModel()
    mplugin = model.getPlugin(SBML_FBC_NAME)
    mplugin.setStrict(True)
    model.setId('{}_fba'.format(model_id))
    model.setName('{} (FBA)'.format(model_id))
    model.setSBOTerm(comp.SBO_FLUX_BALANCE_FRAMEWORK)
    return doc


def template_doc_bounds(model_id, create_min_max=True):
    """ Create template bounds model.

    Adds min and max functions

    :param create_min_max:
    :param model_id: model identifier
    :return: SBMLDocument
    """
    sbmlns = libsbml.SBMLNamespaces(SBML_LEVEL, SBML_VERSION, 'comp', SBML_COMP_VERSION)
    doc = libsbml.SBMLDocument(sbmlns)
    doc.setPackageRequired(SBML_COMP_NAME, True)
    model = doc.createModel()
    model.setId('{}_bounds'.format(model_id))
    model.setName('{} (BOUNDS)'.format(model_id))
    model.setSBOTerm(comp.SBO_CONTINOUS_FRAMEWORK)
    if create_min_max:
        objects = [
         Function('max', 'lambda(x,y, piecewise(x,gt(x,y),y) )', name='min'),
         Function('min', 'lambda(x,y, piecewise(x,lt(x,y),y) )', name='max')]
        factory.create_objects(model, objects)
    return doc


def template_doc_update(model_id):
    """ Create template update model.

    :param model_id: model identifier
    :return: SBMLDocument
    """
    sbmlns = libsbml.SBMLNamespaces(SBML_LEVEL, SBML_VERSION, 'comp', SBML_COMP_VERSION)
    doc = libsbml.SBMLDocument(sbmlns)
    doc.setPackageRequired(SBML_COMP_NAME, True)
    model = doc.createModel()
    model.setId('{}_update'.format(model_id))
    model.setName('{} (UPDATE)'.format(model_id))
    model.setSBOTerm(comp.SBO_CONTINOUS_FRAMEWORK)
    return doc


def template_doc_top(model_id, emds):
    """ Create template top model.
    Adds the ExternalModelDefinitions and submodels for FBA, BOUNDS & UPDATE model.

    :param emds:
    :param model_id: model identifier
    :return: SBMLDocument
    """
    sbmlns = libsbml.SBMLNamespaces(SBML_LEVEL, SBML_VERSION, 'comp', SBML_COMP_VERSION)
    doc = libsbml.SBMLDocument(sbmlns)
    doc.setPackageRequired(SBML_COMP_NAME, True)
    doc.setPackageRequired(SBML_FBC_NAME, False)
    model = doc.createModel()
    model.setId('{}_top'.format(model_id))
    model.setName('{} (TOP)'.format(model_id))
    model.setSBOTerm(comp.SBO_CONTINOUS_FRAMEWORK)
    doc_comp = doc.getPlugin(SBML_COMP_NAME)
    emd_fba = comp.create_ExternalModelDefinition(doc_comp, ('{}_fba'.format(model_id)), source=(emds['{}_fba'.format(model_id)]))
    emd_bounds = comp.create_ExternalModelDefinition(doc_comp, ('{}_bounds'.format(model_id)), source=(emds['{}_bounds'.format(model_id)]))
    emd_update = comp.create_ExternalModelDefinition(doc_comp, ('{}_update'.format(model_id)), source=(emds['{}_update'.format(model_id)]))
    doc_model = model.getPlugin(SBML_COMP_NAME)
    comp.add_submodel_from_emd(doc_model, submodel_id='fba', emd=emd_fba)
    comp.add_submodel_from_emd(doc_model, submodel_id='bounds', emd=emd_bounds)
    comp.add_submodel_from_emd(doc_model, submodel_id='update', emd=emd_update)
    return doc


def create_dfba_compartment(model, compartment_id, unit_volume=None, create_port=True):
    """ Creates the main compartment for the dynamic species.

    :param model:
    :param compartment_id: id
    :param unit_volume: unit
    :param create_port: flag to create port
    :return: created libsbml.Compartment
    """
    objects = [
     Compartment(sid=compartment_id, value=1.0, unit=unit_volume, constant=True, name=compartment_id, spatialDimensions=3,
       port=create_port)]
    sbml_objects = factory.create_objects(model, objects)
    return next(iter(sbml_objects.values()))


def create_biomass_species(model, sid, unit, cf_unit, compartment_id, create_port=True):
    """ Creates the biomass species.

    :param model:
    :return:
    """
    raise NotImplementedError
    fac.create_objects(model, [
     fac.Parameter(sid='cf_X', value=1.0, unit='g_per_mmol', name='biomass conversion factor', constant=True),
     fac.Species(sid='X', value=0.001, compartment='c', name='biomass', substanceUnit='g', hasOnlySubstanceUnits=True, conversionFactor='cf_biomass',
       port=create_port)])


def create_dfba_species(model, model_fba, compartment_id, hasOnlySubstanceUnits=False, unit_amount=None, create_port=True, exclude_sids=[]):
    """ Add DFBA species and compartments from fba model to model.
    Creates the dynamic species and respetive compartments with
    the necessary ports.
    This is used in the bounds submodel, update submodel and the
    and top model.

    :param model:
    :param model_fba:
    :return:
    """
    objects = []
    ex_rids = utils.find_exchange_reactions(model_fba)
    for ex_rid in ex_rids:
        r = model_fba.getReaction(ex_rid)
        sid = r.getReactant(0).getSpecies()
        if sid in exclude_sids:
            pass
        else:
            s = model_fba.getSpecies(sid)
            objects.append(Species(sid=sid, name=(s.getName()), initialConcentration=1.0, substanceUnit=unit_amount, hasOnlySubstanceUnits=hasOnlySubstanceUnits,
              compartment=compartment_id,
              port=create_port))

    factory.create_objects(model, objects)


def create_dfba_dt(model, step_size=DT_SIM, time_unit=None, create_port=True):
    """ Creates the dt parameter in the model.

    :param model:
    :param create_port:
    :param step_size:
    :param time_unit:
    :return:
    """
    objects = [
     Parameter(sid=DT_ID, value=step_size, unit=time_unit, constant=True, sboTerm=DT_SBO, port=create_port)]
    factory.create_objects(model, objects)


def check_exchange_reaction(model, reaction_id):
    """ Checks that the exchange reactions fullfills the necessary specification.

    :param model: SBML model
    :param reaction_id: id of exchange reaction
    :return: boolean true or false
    """
    valid = True
    sid = None
    r = model.getReaction(reaction_id)
    if len(r.getListOfModifiers()) > 0:
        warnings.warn('modfiers set on exchange reaction:'.format(r))
        valid = False
    if len(r.getListOfProducts()) > 0:
        warnings.warn('products set on exchange reaction:'.format(r))
        valid = False
    if len(r.getListOfReactants()) == 0:
        warnings.warn('no reactant set on exchange reaction:'.format(r))
        valid = False
    else:
        if len(r.getListOfReactants()) > 1:
            warnings.warn('more than one reactant set on exchange reaction:'.format(r))
            valid = False
        else:
            sref = r.getReactant(0)
            if abs(sref.getStoichiometry() - 1.0) > 1e-06:
                warnings.warn('stoichiometry of reactant not 1.0 on exchange reaction:'.format(r))
                valid = False
            sid = sref.getSpecies()
        if sid is not None:
            if reaction_id != EXCHANGE_REACTION_PREFIX + sid:
                warnings.warn('exchange reaction id does not follow EX_sid: {} != {}'.format(reaction_id, EXCHANGE_REACTION_PREFIX + sid))
            r.isSetSBOTerm() or warnings.warn('no SBOTerm set on exchange reaction'.format(r))
        elif r.getSBOTermID() != EXCHANGE_REACTION_SBO:
            warnings.warn('exchange reaction id {} != {}:'.format(r.getSBOTermId(), EXCHANGE_REACTION_SBO))
    if not r.getReversible():
        warnings.warn('exchange reaction is not reversible: {}'.format(r))
    return valid


def create_exchange_reaction(model, species_id, exchange_type=EXCHANGE, flux_unit=None):
    """ Factory method to create exchange reactions for species in the FBA model.

    Creates the exchange reaction, the upper and lower bounds,
    and the ports.

    :param model:
    :param species_id:
    :param exchange_type:
    :param flux_unit:

    :return:
    """
    if exchange_type not in [EXCHANGE, EXCHANGE_IMPORT, EXCHANGE_EXPORT]:
        raise ValueError('Wrong exchange_type: {}'.format(exchange_type))
    else:
        ex_rid = EXCHANGE_REACTION_PREFIX + species_id
        lb_id = LOWER_BOUND_PREFIX + ex_rid
        ub_id = UPPER_BOUND_PREFIX + ex_rid
        lb_value = LOWER_BOUND_DEFAULT
        ub_value = UPPER_BOUND_DEFAULT
        if exchange_type == EXCHANGE_IMPORT:
            ub_value = ZERO_BOUND
        if exchange_type == EXCHANGE_EXPORT:
            lb_value = ZERO_BOUND
    parameters = [
     Parameter(sid=lb_id, value=lb_value,
       unit=flux_unit,
       constant=True,
       sboTerm=FLUX_BOUND_SBO,
       port=True),
     Parameter(sid=ub_id, value=ub_value,
       unit=flux_unit,
       constant=True,
       sboTerm=FLUX_BOUND_SBO,
       port=True)]
    factory.create_objects(model, parameters)
    reactions = [
     ExchangeReaction(species_id, reversible=True, lowerFluxBound=lb_id,
       upperFluxBound=ub_id,
       port=True)]
    ex_reactions = factory.create_objects(model, reactions)
    return next(iter(ex_reactions.values()))


def update_exchange_reactions(model, flux_unit):
    """ Updates existing exchange reaction in FBA model.

    Sets all the necessary information and checks that correct.
    This is mainly used to prepare the exchange reactions of metabolites.

    :param flux_unit:
    :param model:
    :return:
    """
    bounds_dict = dict()
    ex_rids = utils.find_exchange_reactions(model)
    for ex_rid in ex_rids:
        r = model.getReaction(ex_rid)
        if not r.getReversible():
            r.setReversible(True)
            logging.info('Exchange reaction set reversible: {}'.format(r.getId()))
        sref = r.getReactant(0)
        sid = sref.getSpecies()
        rid = r.getId()
        if rid != EXCHANGE_REACTION_PREFIX + sid:
            r.setId(EXCHANGE_REACTION_PREFIX + sid)
            logging.warning('Exchange reaction fixd id: {} -> {}'.format(rid, EXCHANGE_REACTION_PREFIX + sid))

    ex_rids = utils.find_exchange_reactions(model)
    for ex_rid in ex_rids:
        r = model.getReaction(ex_rid)
        fbc_r = r.getPlugin(SBML_FBC_NAME)
        for f_bound in ('getLowerFluxBound', 'getUpperFluxBound'):
            bound_id = getattr(fbc_r, f_bound).__call__()
            bound = model.getParameter(bound_id)
            bounds_dict[bound_id] = bound.getValue()

    for ex_rid in ex_rids:
        r = model.getReaction(ex_rid)
        fbc_r = r.getPlugin(SBML_FBC_NAME)
        lb_value = model.getParameter(fbc_r.getLowerFluxBound()).getValue()
        ub_value = model.getParameter(fbc_r.getUpperFluxBound()).getValue()
        lb_id = LOWER_BOUND_PREFIX + ex_rid
        ub_id = UPPER_BOUND_PREFIX + ex_rid
        parameters = [
         Parameter(sid=lb_id, value=lb_value,
           unit=flux_unit,
           constant=True,
           sboTerm=FLUX_BOUND_SBO),
         Parameter(sid=ub_id, value=ub_value,
           unit=flux_unit,
           constant=True,
           sboTerm=FLUX_BOUND_SBO)]
        factory.create_objects(model, parameters)
        fbc.set_flux_bounds(r, lb=lb_id, ub=ub_id)
        comp.create_ports(model, portType=(comp.PORT_TYPE_PORT), idRefs=[
         ex_rid, lb_id, ub_id])

    for ex_rid in ex_rids:
        check_exchange_reaction(model, ex_rid)


def create_update_reactions(model, model_fba, formula='-{}', unit_flux=None, modifiers=None):
    """ Creates all update reactions with the given formula.

    :param model:
    :param model_fba:
    :param formula:
    :param unit_flux:
    :param modifiers:
    :return:
    """
    if modifiers is None:
        modifiers = []
    ex_rids = utils.find_exchange_reactions(model_fba)
    for ex_rid, sid in ex_rids.items():
        create_update_parameter(model=model, sid=sid, unit_flux=unit_flux)
        create_update_reaction(model=model, sid=sid, modifiers=modifiers, formula=formula)


def create_update_reaction(model, sid, modifiers=None, formula='-{}'):
    """ Creates the update reaction for a given species.
    Creates the update parameter in the process.

    :param model:
    :param sid:
    :param modifiers:
    :param formula:
    :return:
    :rtype:
    """
    if modifiers is None:
        modifiers = []
    rid_update = UPDATE_REACTION_PREFIX + sid
    formula = formula.format(FLUX_PARAMETER_PREFIX + sid)
    factory.create_objects(model, [
     Reaction(sid=rid_update,
       sboTerm=UPDATE_REACTION_SBO,
       equation=('{} -> {}'.format(sid, modifiers)),
       formula=(
      formula, None))])


def create_update_parameter(model, sid, unit_flux):
    """ Creates the update parameter.
    The update parameter correspond to the flux parameters
    in the top model.

    :param model:
    :type model:
    :param sid:
    :type sid:
    :param unit_flux:
    :type unit_flux:
    :return: id of parameter
    :rtype:
    """
    pid = FLUX_PARAMETER_PREFIX + sid
    factory.create_objects(model, [
     Parameter(sid=pid, value=1.0, constant=True, unit=unit_flux, sboTerm=UPDATE_PARAMETER_SBO,
       port=True)])
    return pid


def create_exchange_bounds(model_bounds, model_fba, unit_flux=None, create_ports=True):
    """ Creates the exchange reaction flux bounds in the bounds model.

    :param model_bounds: the bounds model submodel
    :param model_fba: the fba submodel
    :param unit_flux: unit of fluxes
    :param create_ports: should ports be created.
    :return:
    """
    ex_rids = utils.find_exchange_reactions(model_fba)
    objects = []
    port_sids = []
    for ex_rid, sid in ex_rids.items():
        r = model_fba.getReaction(ex_rid)
        r_fbc = r.getPlugin(SBML_FBC_NAME)
        lb_id = r_fbc.getLowerFluxBound()
        lb_value = model_fba.getParameter(lb_id).getValue()
        ub_id = r_fbc.getUpperFluxBound()
        ub_value = model_fba.getParameter(ub_id).getValue()
        objects.extend([
         Parameter(sid=lb_id, value=lb_value, unit=unit_flux, constant=False, sboTerm=FLUX_BOUND_SBO),
         Parameter(sid=ub_id, value=ub_value, unit=unit_flux, constant=False, sboTerm=FLUX_BOUND_SBO)])
        port_sids.extend([lb_id, ub_id])

    factory.create_objects(model_bounds, objects)
    if create_ports:
        comp.create_ports(model_bounds, idRefs=port_sids)


def create_dynamic_bounds(model_bounds, model_fba, unit_flux=None):
    """ Creates the dynamic bounds for the model.

    It is necessary to create copies of the fixed bounds from the fba model
    which are subsequently used in the dynamic bounds calculation.

    :return:
    """
    fba_suffix = '_fba'
    objects = []
    ex_rids = utils.find_exchange_reactions(model_fba)
    for ex_rid, sid in ex_rids.items():
        r = model_fba.getReaction(ex_rid)
        r_fbc = r.getPlugin(SBML_FBC_NAME)
        s = model_bounds.getSpecies(sid)
        cid = s.getCompartment()
        ub_id = r_fbc.getUpperFluxBound()
        fba_ub_id = ub_id + fba_suffix
        ub_value = model_fba.getParameter(ub_id).getValue()
        ub_formula = '{}'.format(fba_ub_id)
        objects.extend([
         Parameter(sid=fba_ub_id, value=ub_value, unit=unit_flux, constant=True, sboTerm=FLUX_BOUND_SBO),
         AssignmentRule(sid=ub_id, value=ub_formula, name=('fba export bound ({})'.format(sid)))])
        lb_id = r_fbc.getLowerFluxBound()
        fba_lb_id = lb_id + fba_suffix
        lb_value = model_fba.getParameter(lb_id).getValue()
        if s.getHasOnlySubstanceUnits():
            lb_formula = 'max({}, -{}/dt)'.format(fba_lb_id, sid)
        else:
            lb_formula = 'max({}, -{}*{}/dt)'.format(fba_lb_id, cid, sid)
        objects.extend([
         Parameter(sid=fba_lb_id, value=lb_value, unit=unit_flux, constant=False, sboTerm=FLUX_BOUND_SBO),
         AssignmentRule(sid=lb_id, value=lb_formula, name=('dfba import bound ({})'.format(sid)))])

    factory.create_objects(model_bounds, objects)


def create_dummy_species(model, compartment_id, unit_amount=None, hasOnlySubstanceUnits=False):
    """ Creates the dummy species in the top model.
    Adds a deletion in the top model which removes the object again.

    :param model: SBML model
    :param compartment_id: compartment
    :param unit_amount: unit
    :param hasOnlySubstanceUnits: switch if amount or concentration
    :return:
    """
    objects = [
     Species(sid=DUMMY_SPECIES_ID, name=DUMMY_SPECIES_ID, initialConcentration=0, substanceUnit=unit_amount,
       hasOnlySubstanceUnits=hasOnlySubstanceUnits,
       compartment=compartment_id,
       sboTerm=DUMMY_SPECIES_SBO)]
    factory.create_objects(model, objects)


def create_dummy_reactions(model, model_fba, unit_flux=None):
    """ Creates the dummy reactions.
    This also creates the corresponding flux parameters and flux assignments.

    :param model:
    :param model_fba:
    :param unit_flux:
    :return:
    """
    ex_rids = utils.find_exchange_reactions(model_fba)
    objects = []
    for ex_rid, sid in ex_rids.items():
        pid_flux = FLUX_PARAMETER_PREFIX + sid
        rid_flux = DUMMY_REACTION_PREFIX + sid
        objects = [
         Parameter(sid=pid_flux, value=1.0, constant=True, unit=unit_flux, sboTerm=FLUX_PARAMETER_SBO),
         Reaction(sid=rid_flux, reversible=False, equation=(' -> {}'.format(DUMMY_SPECIES_ID)),
           sboTerm=DUMMY_REACTION_SBO,
           formula=(
          '0 {}'.format(unit_flux), unit_flux)),
         AssignmentRule(pid_flux, value=rid_flux, sboTerm=FLUX_ASSIGNMENTRULE_SBO)]

    factory.create_objects(model, objects)


def create_top_replacedBy(model, model_fba):
    """ Creates the replacedBy Elements in the top model.

    :param model:
    :param model_fba:
    :return:
    """
    ex_rids = utils.find_exchange_reactions(model_fba)
    for ex_rid, sid in ex_rids.items():
        comp.replaced_by(model, (DUMMY_REACTION_PREFIX + sid), ref_type=(comp.SBASE_REF_TYPE_PORT), submodel='fba',
          replaced_by=('{}_port'.format(EXCHANGE_REACTION_PREFIX + sid)))


def create_top_replacements(model, model_fba, compartment_id):
    """ Create all the replacements in the top model.

    :param model:
    :param model_fba:
    :param compartment_id:
    :return:
    """
    comp.replace_elements(model, compartment_id, ref_type=(comp.SBASE_REF_TYPE_PORT), replaced_elements={'update':[
      '{}_port'.format(compartment_id)], 
     'bounds':[
      '{}_port'.format(compartment_id)]})
    comp.replace_elements(model, 'dt', ref_type=(comp.SBASE_REF_TYPE_PORT), replaced_elements={'bounds': ['dt_port']})
    ex_rids = utils.find_exchange_reactions(model_fba)
    for ex_rid, sid in ex_rids.items():
        comp.replace_elements(model, (FLUX_PARAMETER_PREFIX + sid), ref_type=(comp.SBASE_REF_TYPE_PORT), replaced_elements={'update': ['{}_port'.format(FLUX_PARAMETER_PREFIX + sid)]})
        comp.replace_elements(model, sid, ref_type=(comp.SBASE_REF_TYPE_PORT), replaced_elements={'bounds':[
          '{}_port'.format(sid)], 
         'update':[
          '{}_port'.format(sid)]})
        for replace_id in [
         UPPER_BOUND_PREFIX + EXCHANGE_REACTION_PREFIX + sid,
         LOWER_BOUND_PREFIX + EXCHANGE_REACTION_PREFIX + sid]:
            comp.replace_elements(model, replace_id, ref_type=(comp.SBASE_REF_TYPE_PORT), replaced_elements={'bounds':[
              '{}_port'.format(replace_id)], 
             'fba':[
              '{}_port'.format(replace_id)]})

    for unit in model.getListOfUnitDefinitions():
        uid = unit.getId()
        comp.replace_element_in_submodels(model, uid, ref_type=(comp.SBASE_REF_TYPE_UNIT), submodels=[
         'bounds', 'fba', 'update'])